from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class AdminLogin(BaseModel):
    email: EmailStr
    password: str

class Product(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    category: str
    category_id: int
    color: Optional[str] = None
    material: Optional[str] = None
    size: Optional[str] = None

class OrderItem(BaseModel):
    product_id: int
    quantity: int

class CreateOrder(BaseModel):
    user_id: int
    items: List[OrderItem]
    total_amount: float
    status: str = "pending"

class UpdateOrderStatus(BaseModel):
    status: str
