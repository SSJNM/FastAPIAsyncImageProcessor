from fastapi import FastAPI
from routers import defaults,processing
from db import engine
from models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(defaults.router)
app.include_router(processing.router)
