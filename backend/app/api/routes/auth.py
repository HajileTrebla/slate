from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.auth import get_current_user

from app.schemas.user import UserLogin, UserCreate
from app.services.auth_service import register_user, authenticate_user

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register")
async def register(
    payload: UserCreate,
    db: Session = Depends(get_db)
):
    try:
        user = register_user(
            db=db,
            username=payload.username,
            password=payload.password,
            email=payload.email
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    return {
        "message": "User registered successfully",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }


@router.post("/login")
async def login(
    payload: UserLogin,
    db: Session = Depends(get_db)
):
    access_token = authenticate_user(
        db=db,
        identifier=payload.identifier,
        password=payload.password
    )

    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/me")
async def get_me(
    current_user=Depends(get_current_user),
):
    return current_user
