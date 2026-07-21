from uuid import UUID

from pydantic import BaseModel
from datetime import datetime


class TransactionEntryBase(BaseModel):
    transaction_id: UUID
    account_id: UUID
    debit: float | None = None
    credit: float | None = None

class TransactionEntryCreate(TransactionEntryBase):
    pass


class TransactionEntryUpdate(BaseModel):
    transaction_id: UUID | None = None
    account_id: UUID | None = None
    debit: float | None = None
    credit: float | None = None


class TransactionEntryResponse(TransactionEntryBase):
    uuid: UUID

    created_at: datetime
    updated_at: datetime | None = None

    model_config = {
        "from_attributes": True
    }
