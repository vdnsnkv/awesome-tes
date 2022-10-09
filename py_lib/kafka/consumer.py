import logging
from threading import Thread

from confluent_kafka import Consumer

CONSUMER_POLL_TIMEOUT = 0.1

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class KafkaConsumer(object):
    def __init__(
        self,
        brokers: str,
        group_id: str,
        topics: list,
        process_message: callable,
        params: dict = None,
    ):
        if params is None:
            params = {}

        self._consumer = Consumer(
            {
                "bootstrap.servers": brokers,
                "group.id": group_id,
                "logger": logger,
                **params,
            }
        )
        self._consumer.subscribe(topics)

        self._process_message = process_message
        self._is_polling = False
        self._poll_thread = Thread(target=self._run_poll_loop)
        return

    def _run_poll_loop(self):
        logger.info("running consumer poll loop")
        while self._is_polling:
            msg = self._consumer.poll(CONSUMER_POLL_TIMEOUT)
            if msg is None:
                continue
            if msg.error():
                logger.error(f"consumer error: {msg.error()}")
                continue
            self._process_message(msg)
        return

    def start(self):
        logger.info("starting consumer poll loop")
        self._is_polling = True
        self._poll_thread.start()
        return

    def stop(self):
        logger.info("stopping consumer poll loop")
        self._is_polling = False
        self._poll_thread.join()
        return
