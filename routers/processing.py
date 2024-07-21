from fastapi import APIRouter,UploadFile,File,Depends,HTTPException
from typing import List
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from models import Entry,Products
from schemas import EntryCreate,ProductsCreate,EntryFetch
from utils.image_processing import fetch_compress_store_image
import pandas as pd
from db import get_db
import io
import uuid
from core.celery import get_task_info

router = APIRouter(tags=['processing'])

@router.get("/requests/{request_id}", response_model=List[EntryFetch])
def get_entries_by_request_id(request_id: str, db: Session = Depends(get_db)):
    entries = db.query(Entry).filter(Entry.request_id == request_id).all()
    if not entries:
        raise HTTPException(status_code=404, detail="No entries found for the given request ID")
    return entries

@router.get("/task/{task_id}")
async def get_task_status(task_id: str) -> dict:
    """
    Return the status of the submitted Task
    """
    return get_task_info(task_id)

@router.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...),db: Session = Depends(get_db)):
    if file.content_type != 'text/csv':
        return JSONResponse(content={"error": "File type not supported. Please upload a CSV file."}, status_code=400)

    contents = await file.read()
    try:
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

        entries = []
        for index, row in df.iterrows():
            entries.append(EntryCreate(
                product_name=row["ProductName"],
                input_image_url=row["InputImageURL"], 
                status=0
            ))
        request_id = str(uuid.uuid4())
        db_entries = create_entries(db=db, entries=entries, request_id=request_id)

        fetch_compress_store_image(request_id=request_id,entries=entries)
        return db_entries
        # Adding the Celery task to background tasks
        # task = fetch_compress_store_image.apply_async((request_id,entries))
        # return {"task_id": f"The task with id {task.id} is being processed."}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)


def get_product(db: Session, product_name: str):
    return db.query(Products).filter(Products.product_name == product_name).first()

def create_product(db: Session, product: ProductsCreate):
    db_product = Products(product_name=product.product_name)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
 

def create_entry(db: Session, entry: EntryCreate, request_id: str):
    db_entry = Entry(
        request_id=request_id, 
        product_name=entry.product_name, 
        input_image_url=entry.input_image_url, 
        output_image_url=entry.output_image_url,
        status=entry.status
    )
    print(request_id)
    db.add(db_entry)
    db.flush()
    print("1")
    return db_entry

def create_entries(db: Session, entries: List[EntryCreate], request_id: str):
    db_entries = []
    for entry in entries:
        product = get_product(db, entry.product_name)
        if not product:
            product = create_product(db, product=ProductsCreate(product_name=entry.product_name))
        db_entry_id = create_entry(db, entry=entry, request_id=request_id)
        db_entries.append(db_entry_id)
    # print(db_entries)
    db.commit()
    # db.refresh(db_entries)
    def to_dict(instance):
        return {column.name: getattr(instance, column.name) for column in instance.__table__.columns}

    return [to_dict(item) for item in db_entries]


