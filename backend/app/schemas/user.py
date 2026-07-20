from uuid import UUID

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr | None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=255)


class UserResponse(UserBase):
    uuid: UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {
        "from_attributes": True
    }


class UserLogin(BaseModel):
    identifier: str | EmailStr
    password: str = Field(..., min_length=8, max_length=255)
