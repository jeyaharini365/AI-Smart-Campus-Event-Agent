from typing import List, Optional
from bson import ObjectId

from backend.app.core.database import get_database
from backend.app.models.event import EventCreate, EventUpdate, EventDB


class EventRepository:

    @staticmethod
    async def create_event(event: EventCreate, organizer_id: str) -> EventDB:
        db = get_database()

        event_data = event.model_dump()

        new_event = EventDB(
            **event_data,
            organizer_id=ObjectId(organizer_id)
        )

        await db.events.insert_one(
            new_event.model_dump(by_alias=True)
        )

        return new_event

    @staticmethod
    async def get_all_events() -> List[dict]:
        db = get_database()
        events = await db.events.find().to_list(length=None)
        return events

    @staticmethod
    async def get_event_by_id(event_id: str) -> Optional[dict]:
        db = get_database()
        if not ObjectId.is_valid(event_id):
            return None
        event = await db.events.find_one({"_id": ObjectId(event_id)})
        return event

    @staticmethod
    async def update_event(event_id: str, event_update: EventUpdate) -> Optional[dict]:
        db = get_database()
        if not ObjectId.is_valid(event_id):
            return None

        update_data = {k: v for k, v in event_update.model_dump().items() if v is not None}

        if not update_data:
            return await EventRepository.get_event_by_id(event_id)

        await db.events.update_one(
            {"_id": ObjectId(event_id)},
            {"$set": update_data}
        )

        return await EventRepository.get_event_by_id(event_id)

    @staticmethod
    async def delete_event(event_id: str) -> bool:
        db = get_database()
        if not ObjectId.is_valid(event_id):
            return False

        result = await db.events.delete_one({"_id": ObjectId(event_id)})
        return result.deleted_count > 0