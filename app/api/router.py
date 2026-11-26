from fastapi import APIRouter

from app.api import bookings, events

router = APIRouter()
router.include_router(events.router, prefix="/events", tags=["events"])
router.include_router(bookings.router, prefix="/events", tags=["bookings"])
