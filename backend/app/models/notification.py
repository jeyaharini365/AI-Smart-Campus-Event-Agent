from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from backend.app.models.pyobjectid import PyObjectId

class NotificationType(str, Enum):
    INFO = "info"
    ALERT = "alert"
    REMINDER = "reminder"

class NotificationBase(BaseModel):
    user_id: PyObjectId = Field(..., description="Reference to users._id representing target recipient")
    title: str = Field(..., min_length=2, max_length=100)
    message: str = Field(..., min_length=2, max_length=500)
    type: NotificationType = Field(default=NotificationType.INFO)

class NotificationCreate(NotificationBase):
    pass

class NotificationDB(NotificationBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    is_read: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
