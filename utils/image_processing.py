import os 
from celery import shared_task
from PIL import Image
from io import BytesIO
import requests
from db import SessionLocal
from models import Entry
from schemas import EntryCreate
from sqlalchemy.orm import Session
from typing import List
from core.celery import celery_app

IMAGE_STORAGE_PATH = 'output/'
from time import sleep

if not os.path.exists(IMAGE_STORAGE_PATH):
    os.makedirs(IMAGE_STORAGE_PATH)


@celery_app.task
def fetch_compress_store_image(request_id: str, entries: List[EntryCreate], compression_factor: float = 0.5):
    for entry in entries:
        db: Session = SessionLocal()
        try:
            # Update the database entry with the local path
            db: Session = SessionLocal()
            db_entry = db.query(Entry).filter(Entry.input_image_url == entry.input_image_url, Entry.request_id == request_id).first()
            db_entry.status = 1
            db.commit()
            db.refresh(db_entry)

            input_url = entry.input_image_url
            response = requests.get(input_url)
            if response.status_code != 200:
                raise Exception(f"Failed to fetch image from {input_url}")
            content = response.content
            image = Image.open(BytesIO(content))

            # Calculate the new size and compress
            new_size = (int(image.width * compression_factor), int(image.height * compression_factor))
            # Compress the image
            compressed_image = image.resize(new_size, Image.Resampling.LANCZOS)


            # Extracting the file name
            file_name = "output_" + input_url.split("/")[-1]
            local_path = os.path.join(IMAGE_STORAGE_PATH, f"{file_name}")
            compressed_image.save(local_path, format='JPEG')

            # Update the database entry with the local path
            db: Session = SessionLocal()
            db_entry = db.query(Entry).filter(Entry.input_image_url == entry.input_image_url, Entry.request_id == request_id).first()
            db_entry.output_image_url = local_path
            db_entry.status = 2
            db.commit()
            db.refresh(db_entry)

        except Exception as e:
            # Handle exceptions and set status to an error code if needed
            db_entry.status = -1
            db.commit()
            raise e

        finally:
            db.close()
    
