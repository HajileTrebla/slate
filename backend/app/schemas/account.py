from uuid import UUID

from pydantic import BaseModel
from datetime import datetime

from app.enums.account import AccountType


class AccountBase(BaseModel):
    name: str
    account_type: AccountType
    currency: str


class AccountCreate(AccountBase):
    pass


class AccountUpdate(BaseModel):
    uuid: UUID
    name: str | None = None
    account_type: AccountType | None = None
    currency: str | None = None
    is_archived: bool | None = None


class AccountResponse(AccountBase):
    uuid: UUID

    is_archived: bool

    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {
        "from_attributes": True
    }
