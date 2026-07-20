from uuid import UUID

from pydantic import BaseModel
from datetime import datetime

from app.enums.account import AccountType


class AccountBase(BaseModel):
    user_id: UUID
    name: str
    account_type: AccountType


class AccountCreate(AccountBase):
    pass


class AccountResponse(AccountBase):
    uuid: UUID

    is_archived: bool

    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {
        "from_attributes": True
    }
