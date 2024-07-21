from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class EntryBase(BaseModel):
    product_name: str
    input_image_url: str
    output_image_url: Optional[str] = None
    status: int

class EntryCreate(EntryBase):
    
    pass

class EntryFetch(EntryBase):
    id: int
    request_id: str
    
    class Config:
        orm_mode = True

class ProductsBase(BaseModel):
    product_name : str

class Products(ProductsBase):
    id: int
 
    class Config:
        orm_mode = True

class ProductsCreate(ProductsBase):
    pass