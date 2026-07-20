from typing import TYPE_CHECKING
from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.enums.account import AccountType

from app.core.db import Base


if TYPE_CHECKING:
    from app.models.user import User


class Account(Base):
    __tablename__ = "accounts"

    uuid: Mapped[UUID] = mapped_column(
            UUID(as_uuid=True),
            primary_key=True,
            default=uuid4
        )

    user_id: Mapped[UUID] = mapped_column(
            ForeignKey("users.uuid")
        )

    name: Mapped[str] = mapped_column(
            String(100),
            unique=True,
            nullable=False,
            index=True,
        )

    account_type: Mapped[AccountType] = mapped_column(
            String(50),
            nullable=False,
        )
    
    currency: Mapped[str] = mapped_column(
            String(3),
            nullable=False,
            default="PHP"
        )
    
    is_archived: Mapped[bool] = mapped_column(
            nullable=False,
            default=False
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

    user: Mapped["User"] = relationship(
            "User",
            back_populates="accounts"
        )
