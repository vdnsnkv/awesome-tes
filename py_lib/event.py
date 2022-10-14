from enum import Enum

from pydantic import BaseModel


class Event(BaseModel):
    event_name: Enum
    data: dict
