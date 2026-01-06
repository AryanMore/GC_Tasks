from pydantic import BaseModel
from typing import Optional

class Quantity(BaseModel):
    value: float
    unit: str

class Product(BaseModel):
    brand: str
    name: str
    quantity: Quantity
    price: float

class UpdateQuantity(BaseModel):
    value: Optional[float] = None
    unit: Optional[str] = None

class UpdateProduct(BaseModel):
    brand: Optional[str] = None
    name: Optional[str] = None
    quantity: Optional[UpdateQuantity] = None
    price: Optional[float] = None