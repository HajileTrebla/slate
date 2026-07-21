import pytest

from app.services.auth_service import register_user, authenticate_user
from app.core.security import verify_password, decode_access_token

@pytest.mark.unit
def test_register_user(db_session):

    user = register_user(
        db = db_session,
        username = "Test Name",
        email = "test@email.com",
        password = "password123",
    )

    assert user.username == "Test Name"
    assert user.email == "test@email.com"
    assert verify_password("password123", user.password) is True
    

@pytest.mark.unit
def test_authenticate_user(db_session):

    user = register_user(
        db = db_session,
        username = "Test Name",
        email = "test@email.com",
        password = "password123",
    )

    token = authenticate_user(
        db = db_session,
        identifier = "Test Name",
        password = "password123",
    )

    decoded_token = decode_access_token(token)

    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0
    assert str(user.uuid) == decoded_token['sub']
