import enum

from py_lib import Event


class UserStreamingEventType(str, enum.Enum):
    Created = "UserCreated"
    Updated = "UserUpdated"
    Deleted = "UserDeleted"


class UserStreamingEvent(Event):
    event_name: UserStreamingEventType
