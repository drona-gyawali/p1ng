"""
This file contains service level logic for the REST API.
"""

import json
import logging
from typing import Dict

import httpx
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from p1ng.settings import Settings
from p1ng.utils.server_config import test_servers

logger = logging.getLogger(__name__)


async def fetch_ip_details(request: Request):
    headers = request.headers.get("user-agent", "unknown")
    user_ip = request.headers.get("x-forwarded-for", request.client.host).split(",")[0]
    if user_ip.startswith("127.") or user_ip == "localhost":
        user_ip = "103.152.144.29"
    try:
        async with httpx.AsyncClient() as client:
            settings = Settings()
            res = await client.get(settings.ip_details + f"{user_ip}")
            if res.status_code == 200:
                data = res.json()
                country = data.get("country")
                region_name = data.get("regionName")
                status = data.get("status")
                city = data.get("city")
                isp = data.get("isp")
                organization = data.get("org")
                autonomous_system_number = data.get("as")

                logger.info(f"IP Details Fetched for: {user_ip}")

                return JSONResponse(
                    content={
                        "user_agent": headers,
                        "ip": user_ip,
                        "country": country,
                        "region": region_name,
                        "status": status,
                        "city": city,
                        "isp": isp,
                        "organization": organization,
                        "as": autonomous_system_number,
                    }
                )

            else:
                raise HTTPException(
                    status_code=res.status_code,
                    detail=f"Failed to get IP details for {user_ip}",
                )
    except Exception as e:
        logger.exception(f"Failed to fetch details: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error fetching user ip details")


# Expand: This need to expand
async def select_best_server(request: Request) -> Dict:
    try:
        ip_response = await fetch_ip_details(request)
        ip_info = json.loads(ip_response.body.decode("utf-8"))
        user_country = ip_info.get("country")

        if not test_servers:
            raise HTTPException(status_code=503, detail="No available test servers")

        matching_servers = [
            s
            for s in test_servers
            if s.get("location", {}).get("country") == user_country
        ]

        selected = matching_servers[0] if matching_servers else test_servers[0]

        logger.info(
            f"Selected server for country '{user_country}': {selected['name']} ({selected.get('hostname', 'unknown')})"
        )

        return {"selected_server": selected}

    except Exception as e:
        logger.exception(f"Failed to select best server: {str(e)}")
        raise HTTPException(status_code=500, detail="Error selecting best server")
