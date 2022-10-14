import sys

if __package__ is None:
    # this is needed so the script works when it's executed like this `python src/main.py`
    # it is not needed when you use `python -m src.main`
    import os

    DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    sys.path.insert(0, DIR)

from py_lib import KafkaProducerConfig

from app import create_app
from data_streaming import UserStreamingProducer

# SYSLOG_LEVELS = {
#     "CRITICAL": 2,
#     "FATAL": 2,
#     "ERROR": 3,
#     "WARNING": 4,
#     "WARN": 4,
#     "INFO": 6,
#     "DEBUG": 7,
# }

USER_CUD_TOPIC_NAME = "user-streaming"
PRODUCER_CONFIG = KafkaProducerConfig(
    brokers="kafka:9092",
    client_id="user-service-producer",
    params={
        "log_level": 7,
    },
)


if __name__ == "__main__":
    app = create_app()

    user_streaming = UserStreamingProducer(
        USER_CUD_TOPIC_NAME, **PRODUCER_CONFIG.dict()
    )
    user_streaming.start()

    app.user_streaming = user_streaming

    app.run(host="0.0.0.0", port=5050, threaded=True, use_reloader=True)
