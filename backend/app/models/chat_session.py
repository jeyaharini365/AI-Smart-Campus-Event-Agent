from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from backend.app.models.pyobjectid import PyObjectId

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"

class ChatMessage(BaseModel):
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ChatSessionBase(BaseModel):
    user_id: PyObjectId = Field(..., description="Reference to users._id representing user in session")

class ChatSessionCreate(ChatSessionBase):
    pass

class ChatSessionDB(ChatSessionBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    messages: List[ChatMessage] = Field(default_factory=list)
    agent_state: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Serialized memory state used to rehydrate LangGraph execution threads"
    )
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
