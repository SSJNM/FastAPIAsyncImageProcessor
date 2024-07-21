import os
from dotenv import load_dotenv

load_dotenv()  # Load environment from .env file

class Settings:
    MYSQL_HOST: str = os.getenv("MYSQL_HOST")
    MYSQL_USER: str = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD")
    MYSQL_DATABASE: str = os.getenv("MYSQL_DATABASE")
    MYSQL_PORT: str =  os.getenv("MYSQL_PORT")
    RABBITMQ_USER: str = os.getenv("RABBITMQ_USER", "mlteamuser")
    RABBITMQ_PASS: str = os.getenv("RABBITMQ_PASS", "mlteampass")
    RABBITMQ_URL: str = os.getenv("RABBITMQ_URL", "192.168.1.10")
    RABBITMQ_VHOST: str = os.getenv("RABBITMQ_VHOST","mlteamhost")
settings = Settings()

