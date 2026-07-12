from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from sqlalchemy.orm import Session

from app.core.db import get_db

from app.schemas.user import UserLogin
from app.services.auth_service import authenticate_user

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/login")
async def login(
    payload: UserLogin,
    db: Session = Depends(get_db)
):
    user = authenticate_user(
        db=db,
        identifier=payload.identifier,
        password=payload.password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"message": "Login successful"}
