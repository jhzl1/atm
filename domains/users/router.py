from fastapi import APIRouter, Depends
from .schemas import UserCreate
from .service import UserService

users_router = APIRouter(prefix="/users")


@users_router.post("", status_code=201)
async def create_user(user: UserCreate, user_service: UserService = Depends()):
    return await user_service.create_user(user)


@users_router.get("/{user_id}")
async def get_user_by_id(user_id: str, user_service: UserService = Depends()):
    return await user_service.get_user_by_id(user_id)


@users_router.get("/")
async def get_all_users(user_service: UserService = Depends()):
    return await user_service.get_all_users()


@users_router.delete("/{user_id}")
async def delete_user(user_id: str, user_service: UserService = Depends()):
    return await user_service.delete_user(user_id)
