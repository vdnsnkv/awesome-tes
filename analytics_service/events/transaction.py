import enum

from py_lib import Event


class TransactionEventType(str, enum.Enum):
    Created = "TransactionCreated"


class TransactionEvent(Event):
    event_name: TransactionEventType
