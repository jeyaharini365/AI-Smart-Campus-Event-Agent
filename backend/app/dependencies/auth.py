from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from backend.app.core.config import settings
from backend.app.repositories.user_repository import UserRepository
from backend.app.models.user import UserDB

bearer_scheme = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> UserDB:
    token = credentials.credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user_doc = await UserRepository.get_user_by_email(email)
    if user_doc is None:
        raise credentials_exception

    return UserDB(**user_doc)