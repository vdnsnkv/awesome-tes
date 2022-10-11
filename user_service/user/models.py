import enum
from datetime import datetime
from sqlalchemy import (
    Integer,
    Column,
    String,
    DateTime,
    func,
    LargeBinary,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID

from user_service.db import Base


class User(Base):
    __tablename__ = "user"

    @enum.unique
    class Role(enum.Enum):
        DEFAULT = "default"
        ACCOUNTANT = "accountant"
        MANAGER = "manager"
        ADMIN = "admin"

    id = Column(Integer, primary_key=True)
    public_id = Column(
        UUID(as_uuid=True),
        server_default=text("md5(random()::text || clock_timestamp()::text)::uuid"),
        nullable=False,
    )
    email = Column(String, unique=True, nullable=False)
    bcrypt_hash = Column(LargeBinary, nullable=False)

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

    def to_dict(self):
        return {
            "public_id": str(self.public_id),
            "email": self.email,
            "name": self.name,
            "role": self.role,
            "meta": self.meta,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def __repr__(self):
        return f"<{self.__class__.__name__} public_id={self.public_id}>"
