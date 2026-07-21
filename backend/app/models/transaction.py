from typing import TYPE_CHECKING
from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.transaction_entry import TransactionEntry


class Transaction(Base):
    __tablename__="transactions"

    uuid: Mapped[UUID] = mapped_column(
            UUID(as_uuid=True),
            primary_key=True,
            default=uuid4
        )

    date: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )

    description: Mapped[str | None] = mapped_column(
            Text,
            nullable=True
        )

    reference: Mapped[str | None] = mapped_column(
            String(255),
            nullable=True
        )

    created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )

    updated_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
        )

    entries: Mapped[list[TransactionEntry]] = relationship(
        "TransactionEntry",
        back_populates="transaction"
    )
