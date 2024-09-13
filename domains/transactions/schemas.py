from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from datetime import datetime
from bson import ObjectId


class TransactionCreate(BaseModel):
    account: int
    amount: float
    transaction_type: Literal["deposit", "withdraw", "transfer"]
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
        if values.data["transaction_type"] == "transfer" and not v:
            raise ValueError(
                "beneficiary_account is required for transfer transactions"
            )
        if values.data["transaction_type"] != "transfer" and v:
            raise ValueError(
                "beneficiary_account should only be set for transfer transactions"
            )
        return v


class Transaction(TransactionCreate):
    id: Optional[str] = Field(default=None, alias="_id")
    created_at: datetime
    updated_at: datetime

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
