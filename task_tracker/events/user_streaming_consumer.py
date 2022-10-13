import json

from confluent_kafka import Message

from py_lib import DataStreamingConsumer

from .user_cud import (
    USER_CUD_TOPIC_NAME,
    UserCUDEventType,
    UserCUDEvent,
)


class UserStreamingConsumer(DataStreamingConsumer):
    def process_events(self, event: Message):
        if event.event_name == UserCUDEventType.Updated:
            with self.app.app_context():
                user = self.app.user_repo.get_user(event.data["public_id"])
                self.app.user_repo.update_user(user, event.data)
        if event.event_name == UserCUDEventType.Created:
            with self.app.app_context():
                self.app.user_repo.add_user(event.data)
        return
