"""
This file contains the function especially the helper one.
"""

import socket
import time

def run_ping(host: str = "8.8.8.8", port: int = 53, count: int = 4) -> dict:
    latencies = []
    for _ in range(count):
        try:
            start = time.time()
            sock = socket.create_connection((host, port), timeout=2)
            sock.close()
            end = time.time()
            latencies.append((end - start) * 1000)  # ms
        except Exception:
            latencies.append(float('inf'))

    successful = [lat for lat in latencies if lat != float('inf')]
    packet_loss = int((1 - len(successful)/count) * 100)

    if not successful:
        return {
            "ping": None,
            "jitter": None,
            "packet_loss": packet_loss,
            "error": "No successful TCP ping",
        }

    avg_ping = sum(successful) / len(successful)
    diffs = [abs(successful[i] - successful[i-1]) for i in range(1, len(successful))]
    jitter = sum(diffs) / len(diffs) if diffs else 0.0

    return {
        "ping": avg_ping,
        "jitter": jitter,
        "packet_loss": packet_loss,
        "error": None,
    }
