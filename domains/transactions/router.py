from fastapi import APIRouter, Depends, Query
from typing import Optional
from .schemas import TransactionCreate, TransactionType
from .service import TransactionsService

transactions_router = APIRouter(prefix="/transactions", tags=["Transactions"])


@transactions_router.post("", status_code=201, summary="Create a new transaction")
async def deposit(
    transaction: TransactionCreate,
    transactions_services: TransactionsService = Depends(),
):
    return await transactions_services.do_transaction(transaction)


@transactions_router.get(
    "/{account_number}", summary="Get all transactions for a specific account"
)
async def transfer(
    account_number: int,
    type: Optional[TransactionType] = Query(None),
    transactions_services: TransactionsService = Depends(),
):
    return await transactions_services.get_by_account(account_number, type)
