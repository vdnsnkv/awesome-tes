from sqlalchemy import (
    Column,
    String,
    DateTime,
    func,
    Integer,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID

from analytics_service.db import Base


class Task(Base):
    __tablename__ = "task"

    public_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
    )

    user_id = Column(UUID(as_uuid=True))
    title = Column(String)
    jira_id = Column(String)
    description = Column(String)
    status = Column(String)

    assign_price = Column(Integer)
    done_price = Column(Integer)

    meta = Column(JSONB)

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __repr__(self):
        return f"<{self.__class__.__name__} public_id={self.public_id}>"
