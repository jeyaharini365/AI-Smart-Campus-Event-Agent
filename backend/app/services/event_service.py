from fastapi import HTTPException, status

from backend.app.models.event import EventCreate, EventUpdate, EventPublic
from backend.app.models.user import UserDB, UserRole
from backend.app.repositories.event_repository import EventRepository


class EventService:

    @staticmethod
    def _ensure_organizer_or_admin(current_user: UserDB):
        if current_user.role not in (UserRole.ORGANIZER, UserRole.ADMIN):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only organizers or admins can perform this action"
            )

    @staticmethod
    async def create_event(event: EventCreate, current_user: UserDB) -> EventPublic:
        EventService._ensure_organizer_or_admin(current_user)

        new_event = await EventRepository.create_event(event, str(current_user.id))
        return EventPublic(**new_event.model_dump(by_alias=True))

    @staticmethod
    async def get_all_events() -> list[EventPublic]:
        events = await EventRepository.get_all_events()
        return [EventPublic(**event) for event in events]

    @staticmethod
    async def get_event_by_id(event_id: str) -> EventPublic:
        event = await EventRepository.get_event_by_id(event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )
        return EventPublic(**event)

    @staticmethod
    async def update_event(event_id: str, event_update: EventUpdate, current_user: UserDB) -> EventPublic:
        EventService._ensure_organizer_or_admin(current_user)

        existing = await EventRepository.get_event_by_id(event_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )

        updated_event = await EventRepository.update_event(event_id, event_update)
        return EventPublic(**updated_event)

    @staticmethod
    async def delete_event(event_id: str, current_user: UserDB) -> dict:
        EventService._ensure_organizer_or_admin(current_user)

        existing = await EventRepository.get_event_by_id(event_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )

        await EventRepository.delete_event(event_id)
        return {"message": "Event deleted successfully"}