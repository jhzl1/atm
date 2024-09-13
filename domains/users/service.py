from .repository import UserRepository
from .schemas import UserCreate
from fastapi import Depends, HTTPException
import bcrypt
from datetime import datetime
from domains.accounts.service import AccountsService
from bson import ObjectId


class UserService:
    user_repository: UserRepository
    accounts_service: AccountsService

    def __init__(
        self,
        user_repository: UserRepository = Depends(),
        accounts_service: AccountsService = Depends(),
    ):
        self.user_repository = user_repository
        self.accounts_service = accounts_service

    async def create_user(self, user: UserCreate):

        user_email = user.email

        user_exists = await self.user_repository.get_by_email(user_email)

        if user_exists is True:
            raise HTTPException(status_code=400, detail="User already exists")

        account_id = await self.accounts_service.create_account()

        user_dict = dict(user)

        user_dict["password"] = self.hash_password(user.password)
        user_dict["created_at"] = datetime.now()
        user_dict["updated_at"] = datetime.now()
        user_dict["account_id"] = ObjectId(account_id)

        user_id = await self.user_repository.create(user_dict)

        return {"user_id": user_id, "account_id": account_id}

    async def get_user_by_id(self, user_id: str):
        user = await self.user_repository.get_by_id(user_id)

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        user_dict = dict(user)

        del user_dict["account_id"]

        user_account = await self.accounts_service.get_account_by_id(user.account_id)

        return {"user": user_dict, "account": user_account}

    async def get_all_users(self):
        users = await self.user_repository.get_all()

        return users

    async def delete_user(self, user_id: str):

        user = await self.user_repository.get_by_id(user_id)

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        await self.user_repository.delete(user_id)
        await self.accounts_service.delete_account(user.account_id)

        return {"message": "User deleted successfully"}

    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_password.decode("utf-8")
