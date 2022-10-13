from pydantic import BaseModel


class KafkaConsumerConfig(BaseModel):
    brokers: str
    group_id: str
    topics: list[str]
    params: dict = {}


class KafkaProducerConfig(BaseModel):
    brokers: str
    client_id: str
    params: dict = {}
