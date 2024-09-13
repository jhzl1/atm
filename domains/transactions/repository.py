from .schemas import Transaction
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase
from config.database.database import get_db_connection
from bson import ObjectId


class TransactionsRepository:
    db: AsyncIOMotorCollection

    def __init__(self, db: AsyncIOMotorDatabase = Depends(get_db_connection)):
        self.db = db["Transactions"]

    async def create(self, transaction: Transaction) -> str:
        transaction_id = await self.db.insert_one(transaction)

        return str(transaction_id.inserted_id)
