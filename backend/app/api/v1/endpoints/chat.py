from fastapi import APIRouter, Depends
from pydantic import BaseModel

from backend.app.models.user import UserDB
from backend.app.dependencies.auth import get_current_user
from backend.app.agent.graph import run_agent

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest, current_user: UserDB = Depends(get_current_user)):
    reply = await run_agent(request.message, str(current_user.id))
    return ChatResponse(reply=reply)