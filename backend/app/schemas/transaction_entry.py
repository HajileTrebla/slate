from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field
from datetime import datetime


class TransactionEntryBase(BaseModel):
    account_id: UUID
    debit: Decimal | None = Field(default=None, g=0)
    credit: Decimal | None = Field(default=None, g=0)

class TransactionEntryCreate(TransactionEntryBase):
    pass


class TransactionEntryUpdate(BaseModel):
    account_id: UUID | None = None
    debit: Decimal | None = None
    credit: Decimal | None = None


class TransactionEntryResponse(TransactionEntryBase):
    uuid: UUID

    created_at: datetime
    updated_at: datetime | None = None

    model_config = {
        "from_attributes": True
    }
