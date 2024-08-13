from .repository import UserRepository
from .schemas import UserCreate
from config.database.db_access import Database
from fastapi import Depends, HTTPException
import bcrypt
from datetime import datetime


class UserService:
    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository = Depends()):
        self.user_repository = user_repository

    async def create_user(self, user: UserCreate):

        user_email = user.email

        user_exists = await self.user_repository.get_by_email(user_email)

        if user_exists is not None:
            raise HTTPException(status_code=409, detail="User already exists")

        user_dict = dict(user)

        user_dict["password"] = self.hash_password(user.password)
        user_dict["created_at"] = datetime.now()
        user_dict["updated_at"] = datetime.now()

        user_id = await self.user_repository.create(user_dict)

        return {"user_id": user_id}

    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_password.decode("utf-8")
