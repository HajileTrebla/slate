from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=201,
)
async def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
):
    user = User(
        username=payload.username,
        email=payload.email,
        first_name=payload.first_name,
        last_name=payload.last_name,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.get(
        "/",
        response_model=list[UserResponse],
    )
async def get_users(
    db: Session = Depends(get_db)
):
    return db.query(User).all()


@router.get("/{user_id}")
async def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user
