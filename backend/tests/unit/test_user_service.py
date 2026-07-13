import pytest

from app.schemas.user import UserCreate
from app.services.user_service import create_user, get_user, get_users


@pytest.mark.unit
def test_create_user(db_session):

    payload = UserCreate(
            username="j.do",
            email="johndoe@gmail.com",
            password="password123",
    )

    user = create_user(
        db=db_session,
        payload=payload,
    )

    assert user.id is not None


@pytest.mark.unit
def test_get_user(db_session):

    payload = UserCreate(
            username="j.do",
            email="johndoe@gmail.com",
            password="password123",
    )

    created_user = create_user(
        db=db_session,
        payload=payload,
    )

    found_user = get_user(
        db=db_session,
        user_id=created_user.id,
    )

    assert found_user is not None
    assert found_user.id == created_user.id


@pytest.mark.unit
def test_get_users(db_session):

    payload = [
        UserCreate(
                username="j.do",
                email="johndoe@gmail.com",
                password="password123",
            ),
        UserCreate(
                username="sam88",
                email="samson.g01@gmail.com",
                password="password123",
            ),
    ]

    for i in payload:
        create_user(
            db=db_session,
            payload=i,
        )

    users = get_users(db_session)

    assert len(users) == 2


@pytest.mark.unit
def test_get_missing_user(db_session):

    user = get_user(
        db=db_session,
        user_id=99999,
    )

    assert user is None
