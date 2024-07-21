from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings
from sqlalchemy.ext.declarative import declarative_base

MYSQL_USER = settings.MYSQL_USER
MYSQL_HOST = settings.MYSQL_HOST
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_DATABASE = settings.MYSQL_DATABASE
MYSQL_PORT = settings.MYSQL_PORT

if all([MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE]):
    DATABASE_URL = (
        f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    )
else:
    DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()