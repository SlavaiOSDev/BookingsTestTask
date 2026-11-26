from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(
        ForeignKey("events.id"),
        nullable=False,
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    __table_args__ = (
        UniqueConstraint(
            "event_id",
            "user_id",
            name="uq_bookings_event_id_user_id",
        ),
    )


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    capacity: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    __table_args__ = (
        CheckConstraint(
            "capacity > 0",
            name="ck_events_capacity_positive",
        ),
    )
