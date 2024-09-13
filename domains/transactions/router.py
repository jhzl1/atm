from fastapi import APIRouter, Depends
from .schemas import TransactionCreate
from .service import TransactionsService

transactions_router = APIRouter(prefix="/transactions", tags=["Transactions"])


@transactions_router.post("", status_code=201)
async def deposit(
    transaction: TransactionCreate,
    transactions_services: TransactionsService = Depends(),
):
    return await transactions_services.do_transaction(transaction)


@transactions_router.get("/{account_id}")
async def transfer(user_id: str):
    return "hola"

    # return await user_service.get_user_by_id(user_id)


# @transactions_router.get("/")
# async def withdraw(user_service: UserService = Depends()):
#     return await user_service.get_all_users()


# @transactions_router.delete("/{user_id}")
# async def delete_user(user_id: str, user_service: UserService = Depends()):
#     return await user_service.delete_user(user_id)
