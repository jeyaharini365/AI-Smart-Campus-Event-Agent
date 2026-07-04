from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from backend.app.models.pyobjectid import PyObjectId

class UserRole(str, Enum):
    STUDENT = "student"
    ORGANIZER = "organizer"
    ADMIN = "admin"

class UserProfile(BaseModel):
    department: str = Field(..., description="Major department, e.g. Computer Science")
    academic_year: int = Field(..., ge=1, le=5, description="Current academic year (1-5)")
    skills: List[str] = Field(default_factory=list, description="Self-declared technical or non-technical skills")
    interests: List[str] = Field(default_factory=list, description="Preferred event categories or activity interests")

class UserBase(BaseModel):
    email: EmailStr = Field(..., description="Unique campus email address ending in @campus.edu")
    full_name: str = Field(..., min_length=2, max_length=100)
    role: UserRole = Field(default=UserRole.STUDENT)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="Plaintext password to be hashed before saving")
    profile: Optional[UserProfile] = None

class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    profile: Optional[UserProfile] = None

class UserDB(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    hashed_password: str
    profile: Optional[UserProfile] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}

class UserPublic(UserBase):
    id: PyObjectId = Field(alias="_id")
    profile: Optional[UserProfile] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}

class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="Registered campus email address")
    password: str = Field(..., min_length=6, description="Plaintext password to verify")