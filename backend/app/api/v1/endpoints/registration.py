from typing import List
from fastapi import APIRouter, Depends

from backend.app.models.registration import RegistrationCreate, RegistrationPublic
from backend.app.models.user import UserDB
from backend.app.services.registration_service import RegistrationService
from backend.app.dependencies.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=RegistrationPublic)
async def register_for_event(registration: RegistrationCreate, current_user: UserDB = Depends(get_current_user)):
    return await RegistrationService.register_for_event(registration, current_user)

@router.get("/", response_model=List[RegistrationPublic])
async def get_my_registrations(current_user: UserDB = Depends(get_current_user)):
    return await RegistrationService.get_my_registrations(current_user)

@router.delete("/{registration_id}", response_model=RegistrationPublic)
async def cancel_registration(registration_id: str, current_user: UserDB = Depends(get_current_user)):
    return await RegistrationService.cancel_registration(registration_id, current_user)