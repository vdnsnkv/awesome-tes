from py_lib import DataStreamingConsumer, Event

from .transaction import TransactionEventType


class TransactionConsumer(DataStreamingConsumer):
    def process_events(self, event: Event):
        if event.event_name == TransactionEventType.Created:
            with self.app.app_context():
                tr = self.app.transaction_repo.get_transaction(event.data["public_id"])
                if tr is not None:
                    self.app.transaction_repo.update_transaction(tr, event.data)
                    return
                self.app.transaction_repo.add_transaction(event.data)
            return

        return
