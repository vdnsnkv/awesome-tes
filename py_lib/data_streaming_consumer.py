import json
import typing as t
from abc import ABC, abstractmethod

from confluent_kafka import Message
from pydantic import BaseModel

from .kafka.config import KafkaConsumerConfig
from .kafka.consumer import KafkaConsumer


class DataStreamingConsumer(ABC):
    def __init__(
        self, app, event_schema: t.Type[BaseModel], kafka_config: KafkaConsumerConfig
    ):
        self.app = app
        self.event_schema = event_schema
        self.consumer = KafkaConsumer(
            kafka_config,
            process_message=self.process_message,
        )

    def process_message(self, msg: Message):
        event = self.event_schema.parse_obj(json.loads(msg.value()))
        self.process_events(event)
        return

    @abstractmethod
    def process_events(self, event: BaseModel):
        pass

    def start(self):
        self.consumer.start()

    def stop(self):
        self.consumer.stop()
