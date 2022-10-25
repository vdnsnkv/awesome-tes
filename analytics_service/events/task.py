import enum

from py_lib import Event


class TaskEventType(str, enum.Enum):
    Created = "TaskCreated"
    Updated = "TaskUpdated"
    Deleted = "TaskDeleted"


class TaskEvent(Event):
    event_name: TaskEventType
