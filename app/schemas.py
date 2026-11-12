from pydantic import BaseModel, Field
from datetime import datetime

# Base Entities
class EventResponseModel(BaseModel):
    id: int
    name: str
    capacity: int
    created_at: datetime

# POST "/events" - create event
class CreateEventRequestBody(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=255,
        description="Name must be greater than 0 and less 255"
    )
    capacity: int = Field(
        gt=0,
        description="Capacity must be greater than 0"
    )

# GET "/events" - get event
class GetEventsRequestQuery(BaseModel):
    offset: int = Field(
        default=0,
        ge=0,
        description="Offset must be greater or equal 0"
    )
    limit: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Limit must be between 1 and 100"
    )

class GetEventsResponse(BaseModel):
    events: list[EventResponseModel]


# GET "/event/{id}" - get event
class GetEventResponse(BaseModel):
    event: EventResponseModel


# POST "/events/{id}/bookings" - create booking
class CreateBookingRequestBody(BaseModel):
    user_id: int

class CreateBookingResponseModel(BaseModel):
    id: int
    event_name: str
    created_at: datetime
