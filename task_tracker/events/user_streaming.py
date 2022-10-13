import enum

from pydantic import BaseModel


class UserCUDEventType(str, enum.Enum):
    Created = "UserCreated"
    Updated = "UserUpdated"
    Deleted = "UserDeleted"


class UserCUDEvent(BaseModel):
    event_name: UserCUDEventType
    data: dict
