import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    ip_details = os.getenv("IP_URL")
    secret_session = os.getenv("SECRET_KEY")


origins = [
    "http://localhost:3000",
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://localhost",
    "https://drona-gyawali.github.io/",
    "https://p1ng-lbgf.onrender.com", 
    "*",
]
