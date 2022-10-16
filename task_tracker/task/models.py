import enum
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    DateTime,
    func,
    text,
    Integer,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID

from task_tracker.db import Base


class Task(Base):
    __tablename__ = "task"

    @enum.unique
    class Status(enum.Enum):
        TODO = "todo"
        DONE = "done"

    id = Column(Integer, primary_key=True)
    public_id = Column(
        UUID(as_uuid=True),
        server_default=text("md5(random()::text || clock_timestamp()::text)::uuid"),
        nullable=False,
    )

    user_id = Column(UUID(as_uuid=True))
    title = Column(String)
    jira_id = Column(String)
    description = Column(String)
    status = Column(String, default="todo")

    meta = Column(JSONB)

    created_at = Column(DateTime, default=datetime.now, server_default=func.now())
    updated_at = Column(
        DateTime,
        default=datetime.now,
        server_default=func.now(),
        onupdate=datetime.now,
        server_onupdate=func.now(),
    )

    def __repr__(self):
        return f"<{self.__class__.__name__} public_id={self.public_id}>"
