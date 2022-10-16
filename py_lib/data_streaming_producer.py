from .kafka.config import KafkaProducerConfig
from .kafka.producer import KafkaProducer

from .event import Event
from .schema_registry import SchemaRegistry


class DataStreamingProducer:
    def __init__(
        self,
        topic: str,
        kafka_config: KafkaProducerConfig,
        schema_registry: SchemaRegistry,
    ):
        self.topic = topic
        self.name = kafka_config.client_id
        self.producer = KafkaProducer(kafka_config)
        self.schema_registry = schema_registry

    def validate_event(self, event: Event):
        self.schema_registry.validate(
            event.dict(),
            event.event_name.value,
            event.event_version,
        )
        return

    def produce_event(self, event: Event):
        self.producer.produce(self.topic, event.json())
        return

    def start(self):
        self.producer.start()

    def stop(self):
        self.producer.stop()
