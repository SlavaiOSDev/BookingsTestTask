import os

from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, Query
from sqlalchemy import create_engine, insert, select, delete, func
from sqlalchemy.exc import IntegrityError
from typing import Annotated

from app import schemas
from app.models import Event
from app.models import Booking
from app.schemas import EventResponseModel

app = FastAPI()

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "fastapi_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASSWORD", "secret123")

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
engine = create_engine(DATABASE_URL)
events_table = Event.__table__
bookings_table = Booking.__table__


# TODO
# delete /events/{event_id}/bookings/{user_id} //отменить бронирование
#

@app.delete("/events/{event_id}/bookings/{user_id}")
async def delete_booking(
        event_id: int,
        user_id: int
) -> schemas.DeleteBookingResponseModel:
    event_statement = (
        select(events_table)
        .where(events_table.c.id == event_id)
    )

    with engine.begin() as connection:
        event_result = connection.execute(event_statement).one_or_none()

        if event_result is None:
            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )

        booking_statement = (
            delete(bookings_table)
            .where(bookings_table.c.event_id == event_id)
            .where(bookings_table.c.user_id == user_id)
        )

        delete_result = connection.execute(booking_statement)

        if delete_result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Booking not found",
            )

    return schemas.DeleteBookingResponseModel(
        message = "Booking was deleted"
    )



@app.post("/events/{event_id}/bookings", status_code=201)
async def create_booking(
        event_id: int,
        body: schemas.CreateBookingRequestBody
) -> schemas.CreateBookingResponseModel:
    event_statement = (
        select(
            events_table.c.id,
            events_table.c.name,
            events_table.c.capacity,
        )
        .where(events_table.c.id == event_id)
        .with_for_update()
    )

    try:
        with engine.begin() as connection:

            event_result = connection.execute(event_statement).mappings().one_or_none()

            if event_result is None:
                raise HTTPException(
                    status_code=404,
                    detail="Event not found"
                )

            booked_count_statement = (
                select(func.count())
                .select_from(bookings_table)
                .where(bookings_table.c.event_id == event_id)
            )

            booked_count = connection.execute(
                booked_count_statement
            ).scalar_one()

            if booked_count >= event_result["capacity"]:
                raise HTTPException(
                    status_code=409,
                    detail="No available seats",
                )

            booking_statement = (
                insert(bookings_table)
                .values(
                    event_id = event_id,
                    user_id = body.user_id
                )
                .returning(
                    bookings_table.c.id,
                    bookings_table.c.created_at
                )
            )

            booking = (
                connection.execute(booking_statement).mappings().one()
            )

    except IntegrityError as error:
        if error.orig.pgcode == "23505":
            raise HTTPException(
                status_code=409,
                detail="User already has a booking for this event",
            )
        raise

    return schemas.CreateBookingResponseModel(
        id=booking["id"],
        event_name=event_result["name"],
        created_at=booking["created_at"],
    )

@app.get("/events/{event_id}")
async def get_event(event_id: int) -> schemas.GetEventResponse:
    statement = (
        select(events_table)
        .where(events_table.c.id == event_id)
    )

    with engine.connect() as connection:
        result = connection.execute(statement)
        event = result.mappings().one_or_none()

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    event_response: EventResponseModel = schemas.EventResponseModel(
        id = event.id,
        name = event.name,
        capacity = event.capacity,
        created_at = event.created_at
    )
    response: schemas.GetEventResponse = schemas.GetEventResponse(event = event_response)

    return response

@app.get("/events")
async def get_events(query: Annotated[schemas.GetEventsRequestQuery, Query()]) -> schemas.GetEventsResponse:
    statement = (
        select(events_table)
        .order_by(events_table.c.id)
        .offset(query.offset)
        .limit(query.limit)
    )

    with engine.connect() as connection:
        result = connection.execute(statement)
        events = result.mappings().all()

    response: schemas.GetEventsResponse = schemas.GetEventsResponse(events = events)
    return response


@app.post("/events", status_code=201)
async def create_event(event: schemas.CreateEventRequestBody):
    """
    Создание нового ивента
    """

    statement = (
        insert(events_table)
        .values(
            name = event.name,
            capacity = event.capacity
        )
        .returning(
            events_table.c.id,
            events_table.c.name,
            events_table.c.capacity,
            events_table.c.created_at
        )
    )

    with engine.begin() as connection:
        result = connection.execute(statement)
        event = result.mappings().one()

    response = schemas.EventResponseModel(
        id = event.id,
        name = event.name,
        capacity = event.capacity,
        created_at = event.created_at
    )
    return response