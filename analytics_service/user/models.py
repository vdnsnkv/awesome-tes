import enum

from sqlalchemy import (
    Column,
    String,
    DateTime,
    text,
    Integer,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID

from analytics_service.db import Base


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
    email = Column(String)

    name = Column(String)
    role = Column(String)

    balance = Column(Integer)

    meta = Column(JSONB)

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __repr__(self):
        return f"<{self.__class__.__name__} public_id={self.public_id}>"
