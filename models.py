from sqlalchemy import Column, Integer, String, ForeignKey,VARCHAR
from sqlalchemy.orm import relationship
from db import Base

class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(VARCHAR(255), nullable=False)
    product_name = Column(VARCHAR(255), ForeignKey('products.product_name'), nullable=False)
    input_image_url = Column(VARCHAR(255), nullable=False)
    output_image_url = Column(VARCHAR(255), nullable=True)
    status = Column(Integer, nullable=False)
    
    product = relationship("Products", back_populates="entries")


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(VARCHAR(255), unique=True, index=True, nullable=False)
    
    entries = relationship("Entry", back_populates="product")
