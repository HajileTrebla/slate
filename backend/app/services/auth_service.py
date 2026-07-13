from sqlalchemy.orm import Session

from pydantic import EmailStr

from app.models.user import User
from app.core.security import hash_password, verify_password
from app.core.security import create_access_token


def register_user(
    db: Session,
    username: str,
    password: str,
    email: EmailStr | None = None,
) -> User:

    existing_user = {
        db.query(User)
        .filter((User.username == username) | (User.email == email))
        .first()
    }

    if existing_user.pop() is not None:
        raise ValueError(
            "User with this username or email already exists"
        )

    user = User(
        username=username,
        email=email,
        password=hash_password(password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


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
