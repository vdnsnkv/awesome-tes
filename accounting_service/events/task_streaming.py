import enum

from pydantic import BaseModel


class TaskCUDEventType(str, enum.Enum):
    Created = "TaskCreated"
    Updated = "TaskUpdated"
    Deleted = "TaskDeleted"


class TaskCUDEvent(BaseModel):
    event_name: TaskCUDEventType
    data: dict
