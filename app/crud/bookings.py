from sqlalchemy import delete, func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Booking


async def count_bookings_for_event(
    session: AsyncSession,
    event_id: int,
) -> int:
    statement = (
        select(func.count()).select_from(Booking).where(Booking.event_id == event_id)
    )
    result = await session.execute(statement)
    return result.scalar_one()


async def create_booking(
    session: AsyncSession,
    event_id: int,
    user_id: int,
):
    statement = (
        insert(Booking)
        .values(event_id=event_id, user_id=user_id)
        .returning(Booking.id, Booking.created_at)
    )
    result = await session.execute(statement)
    return result.mappings().one()


async def delete_booking(
    session: AsyncSession,
    event_id: int,
    user_id: int,
) -> int:
    statement = (
        delete(Booking)
        .where(Booking.event_id == event_id)
        .where(Booking.user_id == user_id)
    )
    result = await session.execute(statement)
    return result.rowcount
