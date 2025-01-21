from pydantic import BaseModel
from typing import List, Optional

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