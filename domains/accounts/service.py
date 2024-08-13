from .repository import AccountsRepository
from .schemas import Account
import random
from datetime import datetime
from fastapi import Depends, HTTPException


class AccountsService:
    account_repo: AccountsRepository

    def __init__(self, account_repo: AccountsRepository = Depends()):
        self.account_repo = account_repo

    async def create_account(self):
        new_account = Account(
            account_number=random.randint(10000, 99999),
            balance=0.0,
            currency="COP",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        return await self.account_repo.create(dict(new_account))

    async def get_account_by_id(self, account_id: str):
        account = await self.account_repo.get_by_id(account_id)

        if account is None:
            raise HTTPException(status_code=404, detail="Account not found")

        return dict(account)

    async def delete_account(self, account_id: str):
        account = await self.account_repo.get_by_id(account_id)

        if account is None:
            raise HTTPException(status_code=404, detail="Account not found")

        await self.account_repo.delete(account_id)

        return True
