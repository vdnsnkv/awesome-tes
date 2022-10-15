import sys

if __package__ is None:
    # this is needed so the script works when it's executed like this `python src/main.py`
    # it is not needed when you use `python -m src.main`
    import os

    DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    sys.path.insert(0, DIR)

from py_lib import KafkaConsumerConfig

from app import create_app
from events import UserCUDEvent, UserStreamingConsumer
from events import TaskCUDEvent, TaskStreamingConsumer

USER_CUD_TOPIC_NAME = "user-streaming"
USER_CONSUMER_CONFIG = KafkaConsumerConfig(
    brokers="kafka:9092",
    group_id="accounting-service-user-cud-consumer",
    topics=[USER_CUD_TOPIC_NAME],
    params={
        "log_level": 7,
        "auto.offset.reset": "earliest",
    },
)

TASK_CUD_TOPIC_NAME = "task-streaming"
TASK_CONSUMER_CONFIG = KafkaConsumerConfig(
    brokers="kafka:9092",
    group_id="accounting-service-task-cud-consumer",
    topics=[TASK_CUD_TOPIC_NAME],
    params={
        "log_level": 7,
        "auto.offset.reset": "earliest",
    },
)


if __name__ == "__main__":
    app = create_app()

    user_cud_consumer = UserStreamingConsumer(app, UserCUDEvent, USER_CONSUMER_CONFIG)
    user_cud_consumer.start()

    task_cud_consumer = TaskStreamingConsumer(app, TaskCUDEvent, TASK_CONSUMER_CONFIG)
    task_cud_consumer.start()

    app.run(host="0.0.0.0", port=5051, threaded=True, use_reloader=True)
