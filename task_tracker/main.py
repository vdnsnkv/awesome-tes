import sys

if __package__ is None:
    # this is needed so the script works when it's executed like this `python src/main.py`
    # it is not needed when you use `python -m src.main`
    import os

    DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    sys.path.insert(0, DIR)

from py_lib import KafkaConsumerConfig, KafkaProducerConfig, SchemaRegistry

from app import create_app
from task_tracker.events import UserStreamingEvent
from data_streaming import TaskStreamingProducer, UserStreamingConsumer

EVENT_SCHEMAS_DIR = "../event_schemas"

USER_CUD_TOPIC_NAME = "user-streaming"
CONSUMER_CONFIG = KafkaConsumerConfig(
    brokers="kafka:9092",
    group_id="task-tracker-user-cud-consumer",
    topics=[USER_CUD_TOPIC_NAME],
    params={
        "log_level": 7,
        "auto.offset.reset": "earliest",
    },
)

TASK_CUD_TOPIC_NAME = "task-streaming"
PRODUCER_CONFIG = KafkaProducerConfig(
    brokers="kafka:9092",
    client_id="task-tracker-producer",
    params={
        "log_level": 7,
    },
)


if __name__ == "__main__":
    app = create_app()

    schema_registry = SchemaRegistry(EVENT_SCHEMAS_DIR)

    user_cud_consumer = UserStreamingConsumer(
        app,
        UserStreamingEvent,
        CONSUMER_CONFIG,
        schema_registry,
    )
    user_cud_consumer.start()

    task_streaming = TaskStreamingProducer(
        TASK_CUD_TOPIC_NAME,
        PRODUCER_CONFIG,
        schema_registry,
    )
    task_streaming.start()

    app.task_streaming = task_streaming

    app.run(host="0.0.0.0", port=5051, threaded=True, use_reloader=True)
