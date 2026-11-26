from fastapi import APIRouter, status

from app import schemas
from app.db.engine import transaction
from app.services import bookings as bookings_service

router = APIRouter()


@router.delete("/{event_id}/bookings/{user_id}")
async def delete_booking(
    event_id: int,
    user_id: int,
) -> schemas.DeleteBookingResponseModel:
    async with transaction() as session:
        return await bookings_service.delete_booking(
            session=session,
            event_id=event_id,
            user_id=user_id,
        )


@router.post("/{event_id}/bookings", status_code=status.HTTP_201_CREATED)
async def create_booking(
    event_id: int,
    body: schemas.CreateBookingRequestBody,
) -> schemas.CreateBookingResponseModel:
    async with transaction() as session:
        return await bookings_service.create_booking(
            session=session,
            event_id=event_id,
            user_id=body.user_id,
        )
