from typing import List
from fastapi import APIRouter, Depends

from backend.app.models.event import EventCreate, EventUpdate, EventPublic
from backend.app.models.user import UserDB
from backend.app.services.event_service import EventService
from backend.app.dependencies.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=EventPublic)
async def create_event(event: EventCreate, current_user: UserDB = Depends(get_current_user)):
    return await EventService.create_event(event, current_user)

@router.get("/", response_model=List[EventPublic])
async def get_all_events():
    return await EventService.get_all_events()

@router.get("/{event_id}", response_model=EventPublic)
async def get_event(event_id: str):
    return await EventService.get_event_by_id(event_id)

@router.put("/{event_id}", response_model=EventPublic)
async def update_event(event_id: str, event_update: EventUpdate, current_user: UserDB = Depends(get_current_user)):
    return await EventService.update_event(event_id, event_update, current_user)

@router.delete("/{event_id}")
async def delete_event(event_id: str, current_user: UserDB = Depends(get_current_user)):
    return await EventService.delete_event(event_id, current_user)