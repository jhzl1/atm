from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
from bson import ObjectId


class Account(BaseModel):
    currency: Literal["USD", "COP"]
    account: int
    balance: float
    created_at: datetime
    updated_at: datetime

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class AccountCreated(Account):
    id: Optional[str] = Field(alias="_id")
