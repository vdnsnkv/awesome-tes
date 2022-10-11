import enum

from flask import current_app
from pydantic import BaseModel

from user_service.user.models import User

USER_CUD_TOPIC_NAME = "user-streaming"


class UserCUDEventType(str, enum.Enum):
    Created = "UserCreated"
    Updated = "UserUpdated"
    Deleted = "UserDeleted"


class UserCUDEvent(BaseModel):
    event_name: UserCUDEventType
    data: dict


def send_user_cud_event(user: User, event_type: UserCUDEventType):
    event = UserCUDEvent(
        event_name=event_type,
        data=user.to_dict(),
    )
    current_app.producer.produce(USER_CUD_TOPIC_NAME, event.json())
    return
