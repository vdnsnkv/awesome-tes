import logging
import time
from datetime import datetime
from threading import Thread

from .operations import pay_user_balance

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

TIMEOUT = 10.0


class MockedEmailServiceClient:
    def send_user_email(self, *args, **kwargs):
        pass


def _is_day_start():
    now = datetime.utcnow()
    return now.hour == 0 and now.minute == 0


class PaymentsService:
    def __init__(self, app):
        self.app = app
        self.email_client = MockedEmailServiceClient()

        self._today_balances_paid = False

        self._is_running = False
        self._thread = Thread(target=self._run)
        return

    def _make_payments(self):
        try:
            with self.app.app_context():
                all_users = self.app.user_repo.get_all_users()
                users_to_pay = [u for u in all_users if u.balance > 0]

                for user in users_to_pay:
                    transaction = pay_user_balance(user)
                    self.email_client.send_user_email(
                        f"You were paid {transaction.amount} popug money"
                    )
            self._today_balances_paid = True
        except Exception:
            logger.exception("error during making user payments")
            self._today_balances_paid = False

    def _run(self):
        logger.info("running payment service loop")
        while self._is_running:
            if _is_day_start() and not self._today_balances_paid:
                self._make_payments()
            time.sleep(TIMEOUT)
        return

    def start(self):
        logger.info("starting payment service loop")
        self._is_running = True
        self._thread.start()
        return

    def stop(self):
        logger.info("stopping payment service loop")
        self._is_running = False
        self._thread.join()
        return
