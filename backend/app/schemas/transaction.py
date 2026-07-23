from uuid import UUID

from pydantic import BaseModel
from datetime import datetime

from app.schemas.transaction_entry import TransactionEntryCreate, TransactionEntryResponse


class TransactionBase(BaseModel):
    date: datetime
    description: str
    reference: str


class TransactionCreate(TransactionBase):
    entries: list[TransactionEntryCreate] | None = None


class TransactionUpdate(BaseModel):
    date: str | None = None
    description: str | None = None
    reference: str | None = None

    entries: list[TransactionEntryCreate] | None = None


class TransactionResponse(TransactionBase):
    uuid: UUID

    entries: list[TransactionEntryResponse] | None = None

    created_at: datetime
    updated_at: datetime | None = None

    model_config = {
        "from_attributes": True
    }
