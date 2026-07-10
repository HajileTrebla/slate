from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.user import UserCreate, UserResponse

from app.services.user_service import create_user, get_user, get_users

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=201,
)
async def create_user_route(
    payload: UserCreate,
    db: Session = Depends(get_db),
):
    return create_user(
        db=db,
        payload=payload,
    )


@router.get(
        "/",
        response_model=list[UserResponse],
    )
async def get_users_route(
    db: Session = Depends(get_db)
):
    return get_users(
        db=db,
    )


@router.get("/{user_id}")
async def get_user_route(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = get_user(
        db=db,
        user_id=user_id,
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user
