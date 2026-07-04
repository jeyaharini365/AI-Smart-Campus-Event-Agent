from fastapi import APIRouter, Depends

from backend.app.models.user import UserCreate, UserLogin, UserPublic, UserDB
from backend.app.services.user_service import UserService
from backend.app.dependencies.auth import get_current_user

router = APIRouter()

@router.post("/register")
async def register(user: UserCreate):
    return await UserService.register_user(user)

@router.post("/login")
async def login(credentials: UserLogin):
    return await UserService.login_user(credentials)

@router.get("/me")
async def get_me(current_user: UserDB = Depends(get_current_user)):
    return UserPublic(**current_user.model_dump(by_alias=True))