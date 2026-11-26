from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.crud import bookings as bookings_crud
from app.crud import events as events_crud


async def create_booking(
    session: AsyncSession,
    event_id: int,
    user_id: int,
) -> schemas.CreateBookingResponseModel:
    event = await events_crud.get_event(
        session=session,
        event_id=event_id,
        for_update=True,
    )
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    booked_count = await bookings_crud.count_bookings_for_event(
        session=session,
        event_id=event_id,
    )
    if booked_count >= event["capacity"]:
        raise HTTPException(status_code=409, detail="No available seats")

    try:
        booking = await bookings_crud.create_booking(
            session=session,
            event_id=event_id,
            user_id=user_id,
        )
    except IntegrityError as error:
        if getattr(error.orig, "sqlstate", None) == "23505":
            raise HTTPException(
                status_code=409,
                detail="User already has a booking for this event",
            ) from error
        raise

    return schemas.CreateBookingResponseModel(
        id=booking["id"],
        event_name=event["name"],
        created_at=booking["created_at"],
    )


async def delete_booking(
    session: AsyncSession,
    event_id: int,
    user_id: int,
) -> schemas.DeleteBookingResponseModel:
    event = await events_crud.get_event(session=session, event_id=event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    deleted_count = await bookings_crud.delete_booking(
        session=session,
        event_id=event_id,
        user_id=user_id,
    )
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Booking not found")

    return schemas.DeleteBookingResponseModel(message="Booking was deleted")
