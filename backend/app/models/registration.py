from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from backend.app.models.pyobjectid import PyObjectId

class RegistrationStatus(str, Enum):
    REGISTERED = "registered"
    CHECKED_IN = "checked_in"
    CANCELLED = "cancelled"

class RegistrationBase(BaseModel):
    event_id: PyObjectId = Field(..., description="Reference to events._id")
    custom_fields_responses: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Key-value mapping satisfying custom registration fields specified in the event metadata"
    )

class RegistrationCreate(RegistrationBase):
    pass

class RegistrationUpdate(BaseModel):
    status: Optional[RegistrationStatus] = None
    custom_fields_responses: Optional[Dict[str, Any]] = None
    checked_in_at: Optional[datetime] = None

class RegistrationDB(RegistrationBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    student_id: PyObjectId = Field(..., description="Reference to users._id representing student")
    ticket_code: str = Field(..., description="Unique secure hash of ticket used for QR validation")
    status: RegistrationStatus = Field(default=RegistrationStatus.REGISTERED)
    checked_in_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}

class RegistrationPublic(RegistrationBase):
    id: PyObjectId = Field(alias="_id")
    student_id: PyObjectId
    ticket_code: str
    status: RegistrationStatus
    checked_in_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}