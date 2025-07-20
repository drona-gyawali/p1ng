<p align="center">
  <img width="345" height="345" alt="image" src="https://github.com/user-attachments/assets/83cd419e-e503-49eb-b97a-1e92fd49e388" />
</p>


# P1NG – Your Lightweight, Database-less Internet Speed Tester

> **No accounts. No storage. Just raw speed insights.**

---

## 🌐 What is P1NG?

**P1NG** is a simple, database-free speed testing backend service that lets users check their **download speed**, **upload speed**, and **network latency (ping + jitter + packet loss)** — instantly, and without storing any personal data.

### Why P1NG?

* **Database-less** — No user-specific data is stored.
* **Real-time Testing** — Run tests directly from your frontend app.
* **Smart Server Selection** — Auto-selects the best test server (feature-ready).
* **Configurable Backend URLs** — You can easily route your frontend to regional servers (e.g., `np.backend.com` for Nepal or `us.backend.com` for the US).

---

## ⚙️ How It Works (Flow)

1. **Start the Test** from the frontend.
2. The backend:

   * Measures **download** speed by sending a data stream.
   * Accepts **upload** data to evaluate upstream bandwidth.
   * Uses the **ping** endpoint to calculate latency, jitter, and packet loss.
   * Can **fetch your IP details** for extra insights (like ISP and city).
   * Uses the **server selection API** to route to the closest/best location.

> 💡 *We do not store or log your activity. All tests are conducted in real time and forgotten instantly.*

---
### Frontend
> **Note:**
> The backend is production-ready and fully functional. However, the frontend is currently in a prototype phase, primarily showcasing the integration between UI and core services.

> Since we haven't yet deployed global server infrastructure or partnered with server providers, you may not receive the most precise results—especially if you're far from the default server location.

> <img width="1363" height="762" alt="Image" src="https://github.com/user-attachments/assets/2cd20684-91ac-48c9-9e24-e045c8f0b771" />

frontend: [weblink](https://drona-gyawali.github.io/p1ng-ui/)

---



## 🌍 Server Flexibility

We understand running global servers can be costly. That’s why P1NG is built with flexibility in mind.

P1NG supports **dynamic server selection**  the ability to choose the best server based on the user's location only.

> ⚠️ **However, as of now, we do not have any physical server details configured in the backend.**

So while the feature is built and available via the `/select_server` endpoint, **it may not work out of the box unless you add your own servers.**


###  How to Add Your Own  Servers

1. Open the `server_config.py` file in the backend.
2. Add entries for your physical servers like:

```python
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
            "timezone": "Asia/Kathmandu"
        },
        "server_capabilities": {
            "max_bandwidth_mbps": 1000,
            "supports_ipv6": True,
            "ssl_certified": True,
            "uptime_percent": 99.99
        },
        "admin_contact": {
            "name": "Dorna Raj Gyawali",
            "email": "dronarajgyawali.gmail.com"
        },
        "meta": {
            "last_updated": "2025-07-18T12:00:00Z",
            "version": "1.2.0",
            "description": "Community-hosted high-performance test node.",
            "tags": ["community", "lumbini", "nepal", "fast"]
        }
    }
]
```

3. Ensure those backend servers are live and running the P1NG backend service.

Now, the system will automatically route users to the best backend for their location using the `/select_server` API.

---

## 📬 Available REST APIs

| Endpoint         | Method | Description                                               |
| ---------------- | ------ | --------------------------------------------------------- |
| `/ping`          | GET    | Health check – returns `pong` and timestamp               |
| `/download`      | GET    | Measures download speed by streaming random data          |
| `/upload`        | POST   | Accepts upload data and measures upstream speed           |
| `/ping_stats`    | GET    | Returns latency, jitter, and packet loss for a given host |
| `/ip_details`    | POST   | Fetches IP-related info (ISP, city, etc.)                 |
| `/select_server` | POST   | Selects the best available test server         |

---

## 📦 Example Requests & Responses

### Health Check

**GET** `/ping`

```json
{
  "message": "pong",
  "timestamp": 1721383000.0
}
```

---

### ⬇️ Download Test

**GET** `/download?size_mb=5`

* Streams 5MB of random data for speed testing.

---

### ⬆️ Upload Test

**POST** `/upload`

* Uploads any binary stream (up to 100MB).
* **Response:**

```json
{
  "received_bytes": 5242880,
  "status": "ok"
}
```

---

### 📶 Ping Statistics

**GET** `/ping_stats?host=8.8.8.8&count=4`

**Response:**

```json
{
  "ping": 18.34,
  "jitter": 2.5,
  "packet_loss": 0
}
```

---

### 🌍 IP Details

**POST** `/ip_details`

**Response:**

```json
{
  "user_agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
  "ip": "103.152.144.29",
  "country": "Nepal",
  "region": "Lumbini Province",
  "status": "success",
  "city": "Siddharthanagar",
  "isp": "Broad Band Nepal Pvt. Ltd.",
  "organization": "Broad Band Nepal Pvt. Ltd",
  "as": "AS140989 Broad Band Nepal Pvt. Ltd."
}
```

---

### 🧭 Select Server

**POST** `/select_server`

**Response:**

```json
{
  "selected_server": {
    "id": "nep-lumbini-001",
    "name": "p1ng - Lumbini",
    "hostname": "127.0.0.1:8000 ",
    "ip": "103.152.144.29",
    "port": 443,
    "protocols_supported": [
      "https",
      "http",
      "ws"
    ],
    "location": {
      "city": "Butwal",
      "region": "Lumbini Province",
      "country": "Nepal",
      "continent": "Asia",
      "lat": 27.6939,
      "lon": 83.4453,
      "timezone": "Asia/Kathmandu"
    },
    "server_capabilities": {
      "max_bandwidth_mbps": 1000,
      "supports_ipv6": true,
      "ssl_certified": true,
      "uptime_percent": 99.99
    },
    "admin_contact": {
      "name": "Dorna Raj Gyawali",
      "email": "dronarajgyawali.gmail.com"
    },
    "meta": {
      "last_updated": "2025-07-18T12:00:00Z",
      "version": "1.2.0",
      "description": "Community-hosted high-performance test node.",
      "tags": [
        "community",
        "lumbini",
        "nepal",
        "fast"
      ]
    }
  }
}
```

---

## Tech Stack

* **FastAPI** for blazing fast backend performance.
* **No database** — user privacy by design.
* **Streaming APIs** for real-time speed tests.
*  Ready for **multi-region** deployments.
* **Docker** to run and deploy the projects

---

## Final Note

**P1NG** is currently serverless by default. If you’d like to contribute test servers or run your own region-specific backend — you’re welcome! We’ve kept everything lightweight, simple, and fast.
