from .schemas import User
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase
from config.database.database import get_db_connection


class UserRepository:
    db: AsyncIOMotorCollection

    def __init__(self, db: AsyncIOMotorDatabase = Depends(get_db_connection)):
        self.db = db["users"]

    async def create(self, user: User):
        user_id = await self.db.insert_one(user)

        return str(user_id.inserted_id)

    def get_all(self):
        pass

    async def get_by_email(self, user_email: str):
        user = await self.db.find_one({"email": user_email})
        return user if user else None

    def delete(self, user_id: int):
        pass
