from .repository import TransactionsRepository
from .schemas import TransactionCreate, Transaction
from ..accounts.repository import AccountsRepository
from fastapi import Depends, HTTPException
from datetime import datetime


class TransactionsService:
    def __init__(
        self,
        transaction_repository: TransactionsRepository = Depends(),
        account_repository: AccountsRepository = Depends(),
    ):
        self.transaction_repository = transaction_repository
        self.account_repository = account_repository

    async def do_transaction(self, transaction: TransactionCreate) -> dict:

        account_to_update = await self.account_repository.get_by_number(
            transaction.account
        )

        if account_to_update is None:
            raise HTTPException(status_code=404, detail="Account not found")

        if transaction.transaction_type == "withdraw":
            if account_to_update.balance < transaction.amount:
                raise HTTPException(status_code=400, detail="Insufficient funds")
            account_to_update.balance -= transaction.amount

        if transaction.transaction_type == "deposit":
            account_to_update.balance += transaction.amount

        transaction_created = Transaction(
            account=transaction.account,
            amount=transaction.amount,
            beneficiary_account=transaction.beneficiary_account,
            transaction_type=transaction.transaction_type,
            description=transaction.description,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        await self.transaction_repository.create(dict(transaction_created))

        await self.account_repository.update(transaction.account, account_to_update)

        return {"account": account_to_update, "transaction": transaction}
