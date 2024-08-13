from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    identification: int
    password: str


class User(UserCreate):
    id: Optional[str] = Field(alias="_id")
    created_at: datetime
    updated_at: datetime
    account_id: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
