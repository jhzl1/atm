from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    identification: int
    password: str


class User(BaseModel):
    id: Optional[int]
    created_at: datetime
    updated_at: datetime
