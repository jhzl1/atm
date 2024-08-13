from .schemas import User
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase
from config.database.database import get_db_connection
from bson import ObjectId


class UserRepository:
    db: AsyncIOMotorCollection

    def __init__(self, db: AsyncIOMotorDatabase = Depends(get_db_connection)):
        self.db = db["Users"]

    async def create(self, user: User):
        user_id = await self.db.insert_one(user)

        return str(user_id.inserted_id)

    async def get_all(self):
        users = await self.db.find().to_list(1000)

        for user in users:
            user["_id"] = str(user["_id"])
            user["account_id"] = str(user["account_id"])

        return users

    async def get_by_id(self, user_id: str) -> User:
        user = await self.db.find_one({"_id": ObjectId(user_id)})
        if user:
            user["_id"] = str(user["_id"])
            user["account_id"] = str(user["account_id"])
        return User(**user) if user else None

    async def get_by_email(self, user_email: str) -> User:
        user = await self.db.find_one({"email": user_email})

        return True if user else False

    async def delete(self, user_id: int):
        await self.db.delete_one({"_id": ObjectId(user_id)})
        return True
