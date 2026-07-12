from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    email: EmailStr | None
    password: str = Field(..., min_length=8, max_length=255)
    created_at: datetime
    updated_at: datetime


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr | None
    password: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
