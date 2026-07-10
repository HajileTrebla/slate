from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: str | None
    last_name: str | None
    model_config = {
        "from_attributes": True
    }
