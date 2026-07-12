from sqlalchemy.orm import Session
from app.core.security import hash_password

from app.models.user import User
from app.schemas.user import UserCreate


def create_user(
    db: Session,
    payload: UserCreate,
) -> User:

    user = User(
        username=payload.username,
        email=payload.email,
        password=hash_password(payload.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user(
    db: Session,
    user_id: int,
) -> User | None:

    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


def get_users(
    db: Session,
) -> list[User]:

    return db.query(User).all()
