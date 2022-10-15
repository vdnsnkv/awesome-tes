import enum

from py_lib import Event


class TaskStreamingEventType(str, enum.Enum):
    Created = "TaskCreated"
    Updated = "TaskUpdated"
    Deleted = "TaskDeleted"


class TaskStreamingEvent(Event):
    event_name: TaskStreamingEventType
