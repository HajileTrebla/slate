import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from app.main import app
from app.core.db import Base, get_db

from app.core.config import settings

TEST_DATABASE_URL = settings.TEST_DATABASE_URL

engine = create_engine(
    TEST_DATABASE_URL,
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture(scope="session")
def test_db():
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(test_db):
    connection = engine.connect()

    transaction = connection.begin()

    db = TestingSessionLocal(
        bind=connection
    )

    try:
        yield db
    finally:
        db.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(db_session):

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers(client):
    # Register
    client.post(
        "/auth/register",
        json={
            "username": "test_user",
            "email":"test@email.com",
            "password":"password123",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "identifier": "test_user",
            "password": "password123",
    
        },
    )


    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }
