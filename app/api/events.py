from typing import Annotated

from fastapi import APIRouter, Query, status

from app import schemas
from app.db.engine import transaction
from app.services import events as events_service

router = APIRouter()


@router.get("/{event_id}")
async def get_event(event_id: int) -> schemas.GetEventResponse:
    async with transaction() as session:
        return await events_service.get_event(
            session=session,
            event_id=event_id,
        )


@router.get("")
async def get_events(
    query: Annotated[schemas.GetEventsRequestQuery, Query()],
) -> schemas.GetEventsResponse:
    async with transaction() as session:
        return await events_service.get_events(
            session=session,
            offset=query.offset,
            limit=query.limit,
        )


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_event(
    body: schemas.CreateEventRequestBody,
) -> schemas.EventResponseModel:
    async with transaction() as session:
        return await events_service.create_event(
            session=session,
            name=body.name,
            capacity=body.capacity,
        )
