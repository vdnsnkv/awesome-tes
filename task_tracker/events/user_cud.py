import enum

from pydantic import BaseModel

USER_CUD_TOPIC_NAME = "user-service.user-cud.v1"


class UserCUDEventType(str, enum.Enum):
    Created = "User.Created"
    Updated = "User.Updated"
    Deleted = "User.Deleted"


class UserCUDEvent(BaseModel):
    event_name: UserCUDEventType
    data: dict
