from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from backend.app.models.pyobjectid import PyObjectId

class EventCategory(str, Enum):
    WORKSHOP = "workshop"
    SEMINAR = "seminar"
    SPORTS = "sports"
    CULTURAL = "cultural"

class EventStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    CANCELLED = "cancelled"

class FieldType(str, Enum):
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"

class RegistrationField(BaseModel):
    name: str = Field(..., description="Unique key for the dynamic registration field response")
    type: FieldType = Field(default=FieldType.STRING)
    required: bool = Field(default=True)

class FAQItem(BaseModel):
    question: str
    answer: str

class ScheduleItem(BaseModel):
    time_slot: str = Field(..., description="Duration slot, e.g. 10:00 AM - 11:30 AM")
    title: str = Field(..., description="Topic or activity name")
    description: str = Field(..., description="Summary of what the activity entails")
    speaker: Optional[str] = Field(None, description="Name of session conductor")

class EventBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=150)
    description: str = Field(..., min_length=10)
    category: EventCategory
    venue: str = Field(..., min_length=2)
    start_time: datetime
    end_time: datetime
    capacity: int = Field(..., gt=0)

class EventCreate(EventBase):
    registration_fields: List[RegistrationField] = Field(default_factory=list)
    faqs: List[FAQItem] = Field(default_factory=list)
    schedule: List[ScheduleItem] = Field(default_factory=list)

class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=150)
    description: Optional[str] = None
    category: Optional[EventCategory] = None
    venue: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    capacity: Optional[int] = None
    registration_fields: Optional[List[RegistrationField]] = None
    faqs: Optional[List[FAQItem]] = None
    schedule: Optional[List[ScheduleItem]] = None
    status: Optional[EventStatus] = None

class EventDB(EventBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    organizer_id: PyObjectId = Field(..., description="Reference to users._id representing organizer")
    registered_count: int = Field(default=0, ge=0)
    registration_fields: List[RegistrationField] = Field(default_factory=list)
    embedding: Optional[List[float]] = Field(default=None, description="768-dimension Gemini vector embeddings representation")
    faqs: List[FAQItem] = Field(default_factory=list)
    schedule: List[ScheduleItem] = Field(default_factory=list)
    status: EventStatus = Field(default=EventStatus.DRAFT)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}

class EventPublic(EventBase):
    id: PyObjectId = Field(alias="_id")
    organizer_id: PyObjectId
    registered_count: int
    registration_fields: List[RegistrationField]
    faqs: List[FAQItem]
    schedule: List[ScheduleItem]
    status: EventStatus
    created_at: datetime

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}