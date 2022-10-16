import enum

from py_lib import Event


class UserEventType(str, enum.Enum):
    Created = "UserCreated"
    Updated = "UserUpdated"
    Deleted = "UserDeleted"


class UserEvent(Event):
    event_name: UserEventType
