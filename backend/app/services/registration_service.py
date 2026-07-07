from fastapi import HTTPException, status

from backend.app.models.registration import RegistrationCreate, RegistrationPublic
from backend.app.models.user import UserDB
from backend.app.repositories.registration_repository import RegistrationRepository
from backend.app.repositories.event_repository import EventRepository


class RegistrationService:

    @staticmethod
    async def register_for_event(registration: RegistrationCreate, current_user: UserDB) -> RegistrationPublic:
        event_id = str(registration.event_id)

        event = await EventRepository.get_event_by_id(event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )

        if event.get("status") != "published":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This event is not open for registration"
            )

        if event.get("registered_count", 0) >= event.get("capacity", 0):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This event is fully booked"
            )

        existing = await RegistrationRepository.get_registration_by_student_and_event(
            str(current_user.id), event_id
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You are already registered for this event"
            )

        new_registration = await RegistrationRepository.create_registration(
            registration, str(current_user.id)
        )

        return RegistrationPublic(**new_registration.model_dump(by_alias=True))

    @staticmethod
    async def get_my_registrations(current_user: UserDB) -> list[RegistrationPublic]:
        registrations = await RegistrationRepository.get_registrations_by_student(str(current_user.id))
        return [RegistrationPublic(**reg) for reg in registrations]

    @staticmethod
    async def cancel_registration(registration_id: str, current_user: UserDB) -> RegistrationPublic:
        registration = await RegistrationRepository.get_registration_by_id(registration_id)

        if not registration:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registration not found"
            )

        if str(registration["student_id"]) != str(current_user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only cancel your own registration"
            )

        if registration["status"] == "cancelled":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Registration is already cancelled"
            )

        updated = await RegistrationRepository.cancel_registration(
            registration_id, str(registration["event_id"])
        )

        return RegistrationPublic(**updated)

    @staticmethod
    async def get_registrations_for_event(event_id: str, current_user: UserDB) -> list[RegistrationPublic]:
        event = await EventRepository.get_event_by_id(event_id)

        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )

        if str(event["organizer_id"]) != str(current_user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only view registrations for your own events"
            )

        registrations = await RegistrationRepository.get_registrations_by_event(event_id)
        return [RegistrationPublic(**reg) for reg in registrations]