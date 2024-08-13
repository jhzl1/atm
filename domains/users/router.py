from fastapi import APIRouter, Depends
from .schemas import UserCreate
from .service import UserService

users_router = APIRouter(prefix="/users")


@users_router.post("", status_code=201)
async def create_user(user: UserCreate, user_service: UserService = Depends()):

    return await user_service.create_user(user)
