from uuid import UUID

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    email: EmailStr | None
    password: str = Field(..., min_length=8, max_length=255)


class UserResponse(BaseModel):
    uuid: UUID
    username: str
    email: EmailStr | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {
        "from_attributes": True
    }


class UserLogin(BaseModel):
    identifier: str | EmailStr
    password: str = Field(..., min_length=8, max_length=255)
