"""
This file contains the function especially the helper one.
"""

import platform
import re
import subprocess


def run_ping(host: str = "8.8.8.8", count: int = 4) -> dict:
    count_param = "-c" if platform.system() != "Windows" else "-n"
    command = ["ping", count_param, str(count), host]

    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=10)
        output = result.stdout

        times = re.findall(r"time=(\d+\.\d+)", output)
        times = list(map(float, times))

        if not times:
            return {
                "ping": None,
                "jitter": None,
                "packet_loss": None,
                "error": "No ping response found",
            }

        avg_ping = sum(times) / len(times)
        diffs = [abs(times[i] - times[i - 1]) for i in range(1, len(times))]
        jitter = sum(diffs) / len(diffs) if diffs else 0.0

        packet_loss_match = re.search(r"(\d+)% packet loss", output)
        packet_loss = float(packet_loss_match.group(1)) if packet_loss_match else 0.0

        return {
            "ping": avg_ping,
            "jitter": jitter,
            "packet_loss": packet_loss,
            "error": None,
        }

    except Exception as e:
        return {"ping": None, "jitter": None, "packet_loss": None, "error": str(e)}
