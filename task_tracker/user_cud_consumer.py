import json

from confluent_kafka import Message

from py_lib import KafkaConsumer

from task_tracker.events.user_cud import (
    USER_CUD_TOPIC_NAME,
    UserCUDEventType,
    UserCUDEvent,
)

CONSUMER_CONFIG = {
    "brokers": "kafka:9092",
    "group_id": "task-tracker-user-cud-consumer",
    "topics": [USER_CUD_TOPIC_NAME],
    "params": {
        "log_level": 7,
        "auto.offset.reset": "earliest",
    },
}


class UserCUDEventsConsumer:
    def __init__(self, app):
        self.app = app
        self.consumer = KafkaConsumer(
            **CONSUMER_CONFIG, process_message=self.process_user_cud_events
        )

    def process_user_cud_events(self, msg: Message):
        event = UserCUDEvent.parse_obj(json.loads(msg.value()))
        if event.event_name == UserCUDEventType.Updated:
            with self.app.app_context():
                user = self.app.user_repo.get_user(event.data["public_id"])
                self.app.user_repo.update_user(user, event.data)
        if event.event_name == UserCUDEventType.Created:
            with self.app.app_context():
                self.app.user_repo.add_user(event.data)
        return

    def start(self):
        self.consumer.start()
