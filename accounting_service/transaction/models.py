from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    func,
    BigInteger,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID

from accounting_service.db import Base


class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(BigInteger, primary_key=True)
    public_id = Column(
        UUID(as_uuid=True),
        server_default=text("md5(random()::text || clock_timestamp()::text)::uuid"),
        nullable=False,
    )

    user_id = Column(UUID(as_uuid=True))
    task_id = Column(UUID(as_uuid=True))

    amount = Column(BigInteger, nullable=False)

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
