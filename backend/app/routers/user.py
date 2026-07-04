from fastapi import APIRouter

from backend.app.models.user import UserCreate
from backend.app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/register")
async def register(user: UserCreate):
    return await UserService.register_user(user)