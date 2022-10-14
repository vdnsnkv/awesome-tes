import enum

from pydantic import BaseModel


class TaskStreamingEventType(str, enum.Enum):
    Created = "TaskCreated"
    Updated = "TaskUpdated"
    Deleted = "TaskDeleted"


class TaskStreamingEvent(BaseModel):
    event_name: TaskStreamingEventType
    data: dict
