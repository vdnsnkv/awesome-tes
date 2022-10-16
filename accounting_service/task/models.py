from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    DateTime,
    func,
    Integer,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID

from accounting_service.db import Base

from .prices import get_assign_price, get_done_price


class Task(Base):
    __tablename__ = "task"

    public_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
    )

    user_id = Column(UUID(as_uuid=True))
    title = Column(String)

    assign_price = Column(Integer, nullable=False, default=get_assign_price)
    done_price = Column(Integer, nullable=False, default=get_done_price)

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
