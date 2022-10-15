import json
import typing as t
from abc import ABC, abstractmethod

from confluent_kafka import Message
from pydantic import BaseModel

from .kafka.config import KafkaConsumerConfig
from .kafka.consumer import KafkaConsumer

from .event import Event
from .schema_registry import SchemaRegistry


class DataStreamingConsumer(ABC):
    def __init__(
        self,
        app,
        event_schema: t.Type[Event],
        kafka_config: KafkaConsumerConfig,
        schema_registry: SchemaRegistry,
    ):
        self.app = app
        self.event_schema = event_schema
        self.schema_registry = schema_registry
        self.consumer = KafkaConsumer(
            kafka_config,
            process_message=self.process_message,
        )

    def process_message(self, msg: Message):
        data = json.loads(msg.value())

        self.schema_registry.validate(data, data["event_name"], 1)

        event = self.event_schema(**data)

        self.process_events(event)

        return

    @abstractmethod
    def process_events(self, event: Event):
        pass

    def start(self):
        self.consumer.start()

    def stop(self):
        self.consumer.stop()
