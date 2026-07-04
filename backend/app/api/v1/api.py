from fastapi import APIRouter

from backend.app.api.v1.endpoints import user, event, registration, chat

api_router = APIRouter()

api_router.include_router(
    user.router,
    prefix="/users",
    tags=["Users"]
)

api_router.include_router(
    event.router,
    prefix="/events",
    tags=["Events"]
)

api_router.include_router(
    registration.router,
    prefix="/registrations",
    tags=["Registrations"]
)

api_router.include_router(
    chat.router,
    prefix="/chat",
    tags=["Chat"]
)