from typing import Optional
from bson import ObjectId

from backend.app.core.database import get_database
from backend.app.repositories.registration_repository import RegistrationRepository
from backend.app.repositories.event_repository import EventRepository
from backend.app.models.registration import RegistrationCreate


async def search_events(query: Optional[str] = None, category: Optional[str] = None) -> list[dict]:
    """
    Search for published events by keyword (matches title/description) and/or category.
    Only returns events that are open for registration (status = published).
    """
    db = get_database()

    filter_query: dict = {"status": "published"}

    if category:
        filter_query["category"] = category

    if query:
        filter_query["$or"] = [
            {"title": {"$regex": query, "$options": "i"}},
            {"description": {"$regex": query, "$options": "i"}},
        ]

    events = await db.events.find(filter_query).to_list(length=20)

    results = []
    for event in events:
        results.append({
            "event_id": str(event["_id"]),
            "title": event["title"],
            "description": event["description"],
            "category": event["category"],
            "venue": event["venue"],
            "start_time": str(event["start_time"]),
            "end_time": str(event["end_time"]),
            "capacity": event["capacity"],
            "registered_count": event["registered_count"],
            "seats_available": event["capacity"] - event["registered_count"],
        })

    return results


async def register_for_event(student_id: str, event_id: str) -> dict:
    """
    Registers the currently logged-in student for a given event.
    Checks: event exists, is published, has available seats, and student isn't already registered.
    """
    event = await EventRepository.get_event_by_id(event_id)
    if not event:
        return {"success": False, "message": "Event not found."}

    if event.get("status") != "published":
        return {"success": False, "message": "This event is not open for registration."}

    if event.get("registered_count", 0) >= event.get("capacity", 0):
        return {"success": False, "message": "This event is fully booked."}

    existing = await RegistrationRepository.get_registration_by_student_and_event(student_id, event_id)
    if existing:
        return {"success": False, "message": "You are already registered for this event."}

    registration = RegistrationCreate(event_id=ObjectId(event_id), custom_fields_responses={})
    new_registration = await RegistrationRepository.create_registration(registration, student_id)

    return {
        "success": True,
        "message": f"Successfully registered for '{event['title']}'.",
        "registration_id": str(new_registration.id),
        "ticket_code": new_registration.ticket_code,
    }


async def cancel_registration(student_id: str, registration_id: str) -> dict:
    """
    Cancels an existing registration, but only if it belongs to the currently logged-in student.
    """
    registration = await RegistrationRepository.get_registration_by_id(registration_id)

    if not registration:
        return {"success": False, "message": "Registration not found."}

    if str(registration["student_id"]) != student_id:
        return {"success": False, "message": "You can only cancel your own registration."}

    if registration["status"] == "cancelled":
        return {"success": False, "message": "This registration is already cancelled."}

    await RegistrationRepository.cancel_registration(registration_id, str(registration["event_id"]))

    return {"success": True, "message": "Registration cancelled successfully."}


async def view_my_registrations(student_id: str) -> list[dict]:
    """
    Returns all registrations (active and cancelled) belonging to the currently logged-in student,
    along with basic event details for each one.
    """
    registrations = await RegistrationRepository.get_registrations_by_student(student_id)

    results = []
    for reg in registrations:
        event = await EventRepository.get_event_by_id(str(reg["event_id"]))
        results.append({
            "registration_id": str(reg["_id"]),
            "event_title": event["title"] if event else "Unknown event",
            "status": reg["status"],
            "ticket_code": reg["ticket_code"],
            "created_at": str(reg["created_at"]),
        })

    return results