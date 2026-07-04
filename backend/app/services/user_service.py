from fastapi import HTTPException, status

from backend.app.models.user import UserCreate, UserPublic, UserLogin, UserDB
from backend.app.repositories.user_repository import UserRepository
from backend.app.utils.security import verify_password, create_access_token


class UserService:

    @staticmethod
    async def register_user(user: UserCreate):
        existing_user = await UserRepository.get_user_by_email(user.email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        new_user = await UserRepository.create_user(user)

        return UserPublic(**new_user.model_dump(by_alias=True))

    @staticmethod
    async def login_user(credentials: UserLogin):
        user_doc = await UserRepository.get_user_by_email(credentials.email)

        if not user_doc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        user = UserDB(**user_doc)

        if not verify_password(credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email, "role": user.role}
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }