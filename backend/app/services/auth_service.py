from sqlalchemy.orm import Session

from pydantic import EmailStr

from app.models.user import User
from app.core.security import verify_password, create_access_token


def authenticate_user(
    db: Session,
    identifier: str | EmailStr,
    password: str,
) -> User | None:
    user = (
        db.query(User)
        .filter((User.username == identifier) | (User.email == identifier))
        .first()
    )

    if not user:
        return None

    if not verify_password(
        password,
        user.password
    ):
        return None

    return create_access_token(
        subject=str(user.id)
    )
