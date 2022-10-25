import enum

from py_lib import Event


class TaskEventType(str, enum.Enum):
    # data streaming
    Created = "TaskCreated"
    Updated = "TaskUpdated"
    Deleted = "TaskDeleted"

    # business events
    TaskAdded = "TaskAdded"
    TaskAssigned = "TaskAssigned"
    TaskDone = "TaskDone"


class TaskEvent(Event):
    event_name: TaskEventType
