from sqlalchemy import (
    Column,
    DateTime,
    BigInteger,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID

from analytics_service.db import Base


class Transaction(Base):
    __tablename__ = "transaction"

    public_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
    )

    user_id = Column(UUID(as_uuid=True))
    task_id = Column(UUID(as_uuid=True))

    amount = Column(BigInteger)

    meta = Column(JSONB)

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __repr__(self):
        return f"<{self.__class__.__name__} public_id={self.public_id}>"
