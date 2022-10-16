import sys

if __package__ is None:
    # this is needed so the script works when it's executed like this `python src/main.py`
    # it is not needed when you use `python -m src.main`
    import os

    DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    sys.path.insert(0, DIR)

from py_lib import KafkaConsumerConfig, SchemaRegistry

from app import create_app
from events import UserEvent, UserConsumer
from events import TaskEvent, TaskConsumer
from events import TransactionEvent, TransactionConsumer

EVENT_SCHEMAS_DIR = "../event_schemas"

USER_CUD_TOPIC_NAME = "user-streaming"
USER_CONSUMER_CONFIG = KafkaConsumerConfig(
    brokers="kafka:9092",
    group_id="analytics-service",
    topics=[USER_CUD_TOPIC_NAME],
    params={
        "log_level": 7,
        "auto.offset.reset": "earliest",
    },
)

TASK_CUD_TOPIC_NAME = "task-streaming"
TASK_CONSUMER_CONFIG = KafkaConsumerConfig(
    brokers="kafka:9092",
    group_id="analytics-service",
    topics=[TASK_CUD_TOPIC_NAME],
    params={
        "log_level": 7,
        "auto.offset.reset": "earliest",
    },
)


TRANSACTION_CUD_TOPIC_NAME = "transaction-streaming"
TRANSACTION_CONSUMER_CONFIG = KafkaConsumerConfig(
    brokers="kafka:9092",
    group_id="analytics-service",
    topics=[TRANSACTION_CUD_TOPIC_NAME],
    params={
        "log_level": 7,
        "auto.offset.reset": "earliest",
    },
)


if __name__ == "__main__":
    app = create_app()

    schema_registry = SchemaRegistry(EVENT_SCHEMAS_DIR)

    transaction_cud_consumer = TransactionConsumer(
        app,
        TransactionEvent,
        TRANSACTION_CONSUMER_CONFIG,
        schema_registry,
    )
    transaction_cud_consumer.start()

    user_cud_consumer = UserConsumer(
        app, UserEvent, USER_CONSUMER_CONFIG, schema_registry
    )
    user_cud_consumer.start()

    task_cud_consumer = TaskConsumer(
        app, TaskEvent, TASK_CONSUMER_CONFIG, schema_registry
    )
    task_cud_consumer.start()

    app.run(host="0.0.0.0", port=5053, threaded=True, use_reloader=True)
