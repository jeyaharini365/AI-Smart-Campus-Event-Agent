import secrets
from typing import List, Optional
from bson import ObjectId

from backend.app.core.database import get_database
from backend.app.models.registration import RegistrationCreate, RegistrationDB


class RegistrationRepository:

    @staticmethod
    async def get_registration_by_student_and_event(student_id: str, event_id: str) -> Optional[dict]:
        db = get_database()
        registration = await db.registrations.find_one({
            "student_id": ObjectId(student_id),
            "event_id": ObjectId(event_id),
            "status": {"$ne": "cancelled"}
        })
        return registration

    @staticmethod
    async def create_registration(registration: RegistrationCreate, student_id: str) -> RegistrationDB:
        db = get_database()

        registration_data = registration.model_dump()
        ticket_code = secrets.token_hex(8)

        new_registration = RegistrationDB(
            **registration_data,
            student_id=ObjectId(student_id),
            ticket_code=ticket_code
        )

        await db.registrations.insert_one(
            new_registration.model_dump(by_alias=True)
        )

        await db.events.update_one(
            {"_id": ObjectId(str(registration.event_id))},
            {"$inc": {"registered_count": 1}}
        )

        return new_registration

    @staticmethod
    async def get_registrations_by_student(student_id: str) -> List[dict]:
        db = get_database()
        registrations = await db.registrations.find({
            "student_id": ObjectId(student_id)
        }).to_list(length=None)
        return registrations

    @staticmethod
    async def get_registration_by_id(registration_id: str) -> Optional[dict]:
        db = get_database()
        if not ObjectId.is_valid(registration_id):
            return None
        registration = await db.registrations.find_one({"_id": ObjectId(registration_id)})
        return registration

    @staticmethod
    async def cancel_registration(registration_id: str, event_id: str) -> Optional[dict]:
        db = get_database()

        await db.registrations.update_one(
            {"_id": ObjectId(registration_id)},
            {"$set": {"status": "cancelled"}}
        )

        await db.events.update_one(
            {"_id": ObjectId(event_id)},
            {"$inc": {"registered_count": -1}}
        )

        return await RegistrationRepository.get_registration_by_id(registration_id)