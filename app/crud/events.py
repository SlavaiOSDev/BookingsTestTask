from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Event


async def get_event(
    session: AsyncSession,
    event_id: int,
    *,
    for_update: bool = False,
):
    statement = select(Event).where(Event.id == event_id)

    if for_update:
        statement = statement.with_for_update()

    result = await session.execute(statement)
    return result.mappings().one_or_none()


async def get_events(
    session: AsyncSession,
    offset: int,
    limit: int,
):
    statement = select(Event).order_by(Event.id).offset(offset).limit(limit)
    result = await session.execute(statement)
    return result.mappings().all()


async def create_event(
    session: AsyncSession,
    name: str,
    capacity: int,
):
    statement = insert(Event).values(name=name, capacity=capacity).returning(Event)
    result = await session.execute(statement)
    return result.mappings().one()
