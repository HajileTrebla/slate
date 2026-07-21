from uuid import UUID

from pydantic import BaseModel
from datetime import datetime


class TransactionBase(BaseModel):
    date: datetime
    description: str
    reference: str

class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    date: str | None = None
    description: str | None = None
    reference: str | None = None


class TransactionResponse(TransactionBase):
    uuid: UUID

    created_at: datetime
    updated_at: datetime | None = None

    model_config = {
        "from_attributes": True
    }
