import logging
from threading import Thread

from confluent_kafka import Producer

from .config import KafkaProducerConfig

PRODUCER_POLL_TIMEOUT = 0.1

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class KafkaProducer(object):
    def __init__(self, config: KafkaProducerConfig):
        self._producer = Producer(
            {
                "bootstrap.servers": config.brokers,
                "client.id": config.client_id,
                "logger": logger,
                **config.params,
            }
        )
        self._is_polling = False
        self._poll_thread = Thread(target=self._run_poll_loop)
        return

    def _run_poll_loop(self):
        logger.info("running producer poll loop")
        while self._is_polling:
            self._producer.poll(PRODUCER_POLL_TIMEOUT)
        return

    def start(self):
        logger.info("starting producer poll loop")
        self._is_polling = True
        self._poll_thread.start()
        return

    def stop(self):
        logger.info("stopping producer poll loop")
        self._is_polling = False
        self._poll_thread.join()
        return

    @staticmethod
    def _on_delivery(err, msg):
        if err is not None:
            logger.error(f"failed to deliver message: {msg}: {err}")
        else:
            logger.debug(f"message produced: {msg}")

    def produce(self, topic: str, value: str, key: str = None):
        self._producer.produce(
            topic, key=key, value=value, on_delivery=self._on_delivery
        )

        # if poll thread is not started, make poll
        if not self._is_polling:
            self._producer.poll(0)
        return
