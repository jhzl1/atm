from .schemas import Transaction, TransactionType
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase
from config.database.database import get_db_connection
from typing import Optional


class TransactionsRepository:
    db: AsyncIOMotorCollection

    def __init__(self, db: AsyncIOMotorDatabase = Depends(get_db_connection)):
        self.db = db["Transactions"]

    async def create(self, transaction: Transaction) -> str:
        transaction_id = await self.db.insert_one(transaction)

        return str(transaction_id.inserted_id)

    async def get_all_by_account(
        self, account_number: str, transaction_type: Optional[TransactionType] = None
    ):
        query = {"account": account_number}
        if transaction_type:
            query["type"] = transaction_type

        transactions = await self.db.find(query).to_list(1000)

        for transaction in transactions:
            transaction["_id"] = str(transaction["_id"])

        return transactions
