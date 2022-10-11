import enum

from pydantic import BaseModel

USER_CUD_TOPIC_NAME = "user-streaming"


class UserCUDEventType(str, enum.Enum):
    Created = "UserCreated"
    Updated = "UserUpdated"
    Deleted = "UserDeleted"


class UserCUDEvent(BaseModel):
    event_name: UserCUDEventType
    data: dict
