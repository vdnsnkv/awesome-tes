import uuid
from enum import Enum
from datetime import datetime

from pydantic import BaseModel, Field


def event_id():
    return str(uuid.uuid4())


def event_time():
    return datetime.utcnow().isoformat()


class Event(BaseModel):
    event_id: str = Field(default_factory=event_id)
    event_version: int = 1
    event_name: Enum
    event_time: str = Field(default_factory=event_time)
    producer: str
    data: dict
