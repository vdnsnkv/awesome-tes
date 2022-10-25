from py_lib import DataStreamingProducer

from user_service.user.models import User
from user_service.events.user_streaming import (
    UserStreamingEventType,
    UserStreamingEvent,
)


def user_to_event_data(user: User):
    data = {
        "public_id": str(user.public_id),
        "email": user.email,
        "role": user.role,
        "created_at": user.created_at.isoformat(),
        "updated_at": user.updated_at.isoformat(),
    }
    if user.name:
        data["name"] = user.name
    if user.meta:
        data["meta"] = user.meta
    return data


class UserStreamingProducer(DataStreamingProducer):
    def send_event(self, user: User, event_type: UserStreamingEventType):
        event = UserStreamingEvent(
            event_name=event_type,
            producer=self.name,
            data=user_to_event_data(user),
        )
        self.validate_event(event)
        self.produce_event(event)
        return
