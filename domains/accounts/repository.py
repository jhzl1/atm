from .schemas import Account
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase
from config.database.database import get_db_connection
from bson import ObjectId


class AccountsRepository:
    db: AsyncIOMotorCollection

    def __init__(self, db: AsyncIOMotorDatabase = Depends(get_db_connection)):
        self.db = db["Accounts"]

    async def create(self, account: Account) -> str:

        created_account = await self.db.insert_one(account)
        return str(created_account.inserted_id)

    async def get_by_id(self, account_id: str) -> Account:
        account = await self.db.find_one({"_id": ObjectId(account_id)})
        if account:
            account["_id"] = str(account["_id"])
        return Account(**account) if account else None

    async def delete(self, account_id: int):
        await self.db.delete_one({"_id": ObjectId(account_id)})
        return True

    # async def get_by_email(self, user_email: str) -> User:
    #     user = await self.db.find_one({"email": user_email})
    #     if user:
    #         user["_id"] = str(user["_id"])
    #     return User(**user) if user else None
