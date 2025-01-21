from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class AuthDTO(BaseModel):
    username: str
    password: str

class CurrentUserDTO(BaseModel):
    user_id: str
    role: str



class ProductDTO(BaseModel):
    name: str
    price: float
    quantity: int

class OrderCreateDTO(BaseModel):
    customer_name: str
    products: List[ProductDTO]



class OrderStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"

class OrderUpdateDTO(BaseModel):
    status: Optional[OrderStatus] = None
    products: Optional[List[ProductDTO]] = None