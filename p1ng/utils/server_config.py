"""
This file contains the details of the available test servers.
You can add new server entries here to expand support for more regions.

The selection logic ensures that each user is automatically connected to the most geographically
appropriate server, providing a more accurate and region-optimized speed test experience.
"""

# dummy config template
test_servers = [
    {
        "id": "nep-lumbini-001",
        "name": "p1ng - Lumbini",
        "hostname": "127.0.0.1:8000 ",
        "ip": "103.152.144.29",
        "port": 443,
        "protocols_supported": ["https", "http", "ws"],
        "location": {
            "city": "Butwal",
            "region": "Lumbini Province",
            "country": "Nepal",
            "continent": "Asia",
            "lat": 27.6939,
            "lon": 83.4453,
            "timezone": "Asia/Kathmandu",
        },
        "server_capabilities": {
            "max_bandwidth_mbps": 1000,
            "supports_ipv6": True,
            "ssl_certified": True,
            "uptime_percent": 99.99,
        },
        "admin_contact": {
            "name": "Dorna Raj Gyawali",
            "email": "dronarajgyawali.gmail.com",
        },
        "meta": {
            "last_updated": "2025-07-18T12:00:00Z",
            "version": "1.2.0",
            "description": "Community-hosted high-performance test node.",
            "tags": ["community", "lumbini", "nepal", "fast"],
        },
    }
]
