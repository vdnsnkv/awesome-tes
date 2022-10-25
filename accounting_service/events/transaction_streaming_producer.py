from py_lib import DataStreamingProducer

from accounting_service.transaction.models import Transaction
from accounting_service.events.transaction import (
    TransactionEvent,
    TransactionEventType,
)


def transaction_to_event_data(tr: Transaction):
    data = {
        "public_id": str(tr.public_id),
        "user_id": str(tr.user_id),
        "task_id": str(tr.task_id),
        "amount": tr.amount,
        "created_at": tr.created_at.isoformat(),
        "updated_at": tr.updated_at.isoformat(),
    }
    if tr.meta:
        data["meta"] = tr.meta
    return data


class TransactionStreamingProducer(DataStreamingProducer):
    def send_event(self, tr: Transaction):
        event = TransactionEvent(
            event_name=TransactionEventType.Created,
            producer=self.name,
            data=transaction_to_event_data(tr),
        )
        self.validate_event(event)
        self.produce_event(event)
        return
