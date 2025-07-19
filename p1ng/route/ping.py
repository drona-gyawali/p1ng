"""
This file contains all the apis that used in the project.

For further details kindly visit: http://127.0.0.1:8000/docs
"""

import logging
import os
import time

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import StreamingResponse
from pydantic import conint, constr

from p1ng.service.ping import fetch_ip_details, select_best_server
from p1ng.utils.ping_utils import run_ping

# Configure logging
logger = logging.getLogger(__name__)
router = APIRouter(tags=["Test Speed"])

MAX_DOWNLOAD_SIZE_MB = 100
MAX_UPLOAD_SIZE_MB = 100
MAX_PING_COUNT = 20
MIN_PING_COUNT = 1


@router.get("/ping")
async def health_check():
    """Endpoint for service health verification"""
    return {"message": "pong", "timestamp": time.time()}


@router.get("/download")
async def download(size_mb: conint(ge=1, le=MAX_DOWNLOAD_SIZE_MB) = 5):  # type: ignore
    """Generate downloadable test data with size validation"""
    size_bytes = size_mb * 1024 * 1024

    def data_generator():
        chunk_size = 1024 * 1024  # 1MB chunks
        bytes_sent = 0
        while bytes_sent < size_bytes:
            chunk = os.urandom(min(chunk_size, size_bytes - bytes_sent))
            yield chunk
            bytes_sent += len(chunk)

    return StreamingResponse(
        data_generator(),
        media_type="application/octet-stream",
        headers={"Content-Length": str(size_bytes)},
    )


@router.post("/upload")
async def upload(request: Request):
    """Process uploaded data with size validation"""
    MAX_SIZE = MAX_UPLOAD_SIZE_MB * 1024 * 1024
    received_bytes = 0

    async for chunk in request.stream():
        received_bytes += len(chunk)
        if received_bytes > MAX_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File exceeds maximum size ({MAX_UPLOAD_SIZE_MB}MB)",
            )

    return {
        "received_bytes": received_bytes,
        "status": "ok" if received_bytes > 0 else "empty",
    }


@router.post("/ip_details")
async def ip_detail(request: Request):
    """Fetch IP details with error handling"""
    try:
        return await fetch_ip_details(request)
    except Exception as e:
        logger.error(f"IP detail error: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not retrieve IP information")


@router.get("/ping_stats")
async def ping_stats(
    host: constr(pattern=r"^[a-zA-Z0-9.-]+$") = Query("8.8.8.8", description="Host to ping"),  # type: ignore
    count: conint(ge=MIN_PING_COUNT, le=MAX_PING_COUNT) = Query(4, description="Number of ping packets"),  # type: ignore
):
    """Get network ping statistics with input validation"""
    try:
        stats = run_ping(host=host, count=count)
    except Exception as e:
        logger.error(f"Ping error for {host}: {str(e)}")
        raise HTTPException(status_code=500, detail="Network measurement failed")

    if stats.get("error"):
        raise HTTPException(status_code=400, detail=stats["error"])

    return {
        "ping": round(stats["ping"], 2),
        "jitter": round(stats["jitter"], 2),
        "packet_loss": stats["packet_loss"],
    }


@router.post("/select_server")
async def select_server(request: Request):
    try:
        server_details = await select_best_server(request)
        return server_details
    except Exception as e:
        logger.error(f"Error selecting server: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to select server")
