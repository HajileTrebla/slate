from typing import TYPE_CHECKING
from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, DateTime, ForeignKey, Float, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


if TYPE_CHECKING:
    from app.models.transaction import Transaction
    from app.models.account import Account


class TransactionEntry(Base):
    __tablename__ = "transaction_entries"

    uuid: Mapped[UUID] = mapped_column(
            UUID(as_uuid=True),
            primary_key=True,
            default=uuid4
        )

    transaction_id: Mapped[UUID] = mapped_column(
            ForeignKey("transactions.uuid")
        )

    account_id: Mapped[UUID] = mapped_column(
            ForeignKey("accounts.uuid")
        )
    
    debit: Mapped[float] = mapped_column(
            Float(),
            default=0.00,
            nullable=False,
        )

    credit: Mapped[float] = mapped_column(
            Float(),
            default=0.00,
            nullable=False,
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

    transaction: Mapped["Transaction"] = relationship(
            "Transaction",
            back_populates="transaction_entry"
        )

    accounts: Mapped["Account"] = relationship(
            "Account",
            back_populates="transaction_entry"
        )
