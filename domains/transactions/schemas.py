from enum import Enum
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from bson import ObjectId


class TransactionType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"
    TRANSFER = "TRANSFER"


class TransactionCreate(BaseModel):
    account: int
    amount: float
    type: TransactionType
    description: Optional[str] = None
    beneficiary_account: Optional[int] = None

    @field_validator("amount")
    @classmethod
    def amount_must_be_greater_than_one(cls, v):
        if v == 0:
            raise ValueError("amount must be greater than zero")
        return v

    @field_validator("beneficiary_account", mode="before")
    @classmethod
    def check_beneficiary_account_id(cls, v, values):
        if values.data["type"] == "TRANSFER" and not v:
            raise ValueError(
                "beneficiary_account is required for transfer transactions"
            )
        if values.data["type"] != "TRANSFER" and v:
            raise ValueError(
                "beneficiary_account should only be set for transfer transactions"
            )
        return v


class Transaction(TransactionCreate):
    created_at: datetime
    updated_at: datetime

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class TransactionCreated(Transaction):
    id: Optional[str] = Field(alias="_id")
