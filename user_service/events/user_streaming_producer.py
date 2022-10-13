from py_lib import DataStreamingProducer

from user_service.user.models import User
from user_service.events.user_cud import UserCUDEventType, UserCUDEvent


class UserStreamingProducer(DataStreamingProducer):
    def send_event(self, user: User, event_type: UserCUDEventType):
        event = UserCUDEvent(
            event_name=event_type,
            data=user.to_dict(),
        )
        super().send_event(event)
        return
