import enum
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    DateTime,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID

from accounting_service.db import Base


class User(Base):
    __tablename__ = "user"

    @enum.unique
    class Role(enum.Enum):
        DEFAULT = "default"
        ACCOUNTANT = "accountant"
        MANAGER = "manager"
        ADMIN = "admin"

    public_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("md5(random()::text || clock_timestamp()::text)::uuid"),
        nullable=False,
    )
    email = Column(String, unique=True, nullable=False)

    name = Column(String)
    role = Column(String, default="default")

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
