from .repository import TransactionsRepository
from .schemas import TransactionCreate, Transaction, TransactionType
from ..accounts.repository import AccountsRepository
from fastapi import Depends, HTTPException
from datetime import datetime
from typing import Optional


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

        if transaction.type == TransactionType.WITHDRAW:
            if account_to_update.balance < transaction.amount:
                raise HTTPException(status_code=400, detail="Insufficient funds")
            account_to_update.balance -= transaction.amount

        if transaction.type == TransactionType.DEPOSIT:
            account_to_update.balance += transaction.amount

        if transaction.type == TransactionType.TRANSFER:
            beneficiary_account = await self.account_repository.get_by_number(
                transaction.beneficiary_account
            )
            if beneficiary_account is None:
                raise HTTPException(
                    status_code=404, detail="Beneficiary account not found"
                )
            if account_to_update.balance < transaction.amount:
                raise HTTPException(status_code=400, detail="Insufficient funds")

            account_to_update.balance -= transaction.amount

            beneficiary_account.balance += transaction.amount

            await self.account_repository.update(
                transaction.beneficiary_account, beneficiary_account
            )

        transaction_created = Transaction(
            account=transaction.account,
            amount=transaction.amount,
            beneficiary_account=transaction.beneficiary_account,
            type=transaction.type,
            description=transaction.description,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        await self.transaction_repository.create(dict(transaction_created))

        await self.account_repository.update(transaction.account, account_to_update)

        return {"account": account_to_update, "transaction": transaction}

    async def get_by_account(
        self, account_number: int, transaction_type: Optional[TransactionType] = None
    ):
        account = await self.account_repository.get_by_number(account_number)

        if account is None:
            raise HTTPException(status_code=404, detail="Account not found")

        transactions = await self.transaction_repository.get_all_by_account(
            account_number, transaction_type
        )

        return transactions
