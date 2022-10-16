from .kafka.config import KafkaProducerConfig
from .kafka.producer import KafkaProducer


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

    def validate_event(self, event: Event):
        pass

    def produce_event(self, event: Event):
        self.producer.produce(self.topic, event.json())
        return

    def start(self):
        self.producer.start()

    def stop(self):
        self.producer.stop()
