from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.crud import events as events_crud


async def get_event(
    session: AsyncSession,
    event_id: int,
) -> schemas.GetEventResponse:
    event = await events_crud.get_event(
        session=session,
        event_id=event_id,
    )

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    return schemas.GetEventResponse(event=schemas.EventResponseModel(**event))


async def get_events(
    session: AsyncSession,
    offset: int,
    limit: int,
) -> schemas.GetEventsResponse:
    events = await events_crud.get_events(
        session=session,
        offset=offset,
        limit=limit,
    )
    return schemas.GetEventsResponse(
        events=[schemas.EventResponseModel(**event) for event in events],
    )


async def create_event(
    session: AsyncSession,
    name: str,
    capacity: int,
) -> schemas.EventResponseModel:
    event = await events_crud.create_event(
        session=session,
        name=name,
        capacity=capacity,
    )
    return schemas.EventResponseModel(**event)
