from pydantic import BaseModel

from .kafka.config import KafkaProducerConfig
from .kafka.producer import KafkaProducer


class DataStreamingProducer:
    def __init__(self, topic: str, kafka_config: KafkaProducerConfig):
        self.topic = topic
        self.producer = KafkaProducer(**kafka_config.dict())

    def produce_event(self, event: BaseModel):
        self.producer.produce(self.topic, event.json())
        return

    def start(self):
        self.producer.start()

    def stop(self):
        self.producer.stop()
