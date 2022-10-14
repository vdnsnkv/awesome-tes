import enum

from pydantic import BaseModel


class UserStreamingEventType(str, enum.Enum):
    Created = "UserCreated"
    Updated = "UserUpdated"
    Deleted = "UserDeleted"


class UserStreamingEvent(BaseModel):
    event_name: UserStreamingEventType
    data: dict
