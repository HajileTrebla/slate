from typing import TYPE_CHECKING
from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from backend.app.models.account import Account


class User(Base):
    __tablename__ = "users"

    uuid: Mapped[UUID] = mapped_column(
            UUID(as_uuid=True),
            primary_key=True,
            default=uuid4
        )

    username: Mapped[str] = mapped_column(
            String(50),
            unique=True,
            nullable=False,
            index=True,
        )

    email: Mapped[str | None] = mapped_column(
            String(255),
            unique=True,
            nullable=True,
        )

    password: Mapped[str] = mapped_column(
            String(255),
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

    accounts: Mapped[list["Account"]] = relationship(
            "Account",
            back_populates="user"
        )
