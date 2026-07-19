from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException

from app.core.db import get_db
from app.core.security import decode_access_token
from app.models.user import User

import jwt

oauth2_scheme = OAuth2PasswordBearer(
        tokenUrl="/auth/login"
    )


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    try:
        payload = decode_access_token(token)

        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.get(
        User,
        user_id
    )

    if not user:
        raise HTTPException(
                status_code=404,
                detail="User not found"
            )

    return user
