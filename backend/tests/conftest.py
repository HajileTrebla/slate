import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from app.main import app
from app.core.db import Base, get_db
from app.core.config import settings

from app.models.user import User
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.transaction_entry import TransactionEntry

from app.enums.account import AccountType


TEST_DATABASE_URL = settings.TEST_DATABASE_URL

engine = create_engine(TEST_DATABASE_URL)

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

    db = TestingSessionLocal(bind=connection)

    try:
        yield db
    finally:
        db.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(db_session):

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers(client):

    client.post(
        "/auth/register",
        json={
            "username": "test_user",
            "email": "test@email.com",
            "password": "password123",
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


@pytest.fixture
def test_user(db_session, auth_headers):
    """
    Returns the same user created during registration.
    """

    return (
        db_session.query(User)
        .filter(User.username == "test_user")
        .first()
    )


@pytest.fixture
def account_factory(
    db_session,
    test_user,
):
    def factory(
        *,
        name="Test Account",
        account_type=AccountType.ASSET,
        currency="PHP",
        is_archived=False,
    ):

        account = Account(
            user_id=test_user.uuid,
            name=name,
            account_type=account_type,
            currency=currency,
            is_archived=is_archived,
        )

        db_session.add(account)
        db_session.commit()
        db_session.refresh(account)

        return account

    return factory


@pytest.fixture
def transaction_factory(
    db_session,
    account_factory,
):
    def factory(
        *,
        description="Test Transaction",
        reference="REF-001",
        date=None,
        entries=None,
    ):

        from datetime import datetime

        transaction = Transaction(
            description=description,
            reference=reference,
            date=date or datetime.utcnow(),
        )

        db_session.add(transaction)
        db_session.flush()

        if entries:
            for entry in entries:

                account = entry.get("account")

                if account is None:
                    account = account_factory()

                transaction.entries.append(
                    TransactionEntry(
                        account_id=account.uuid,
                        debit=entry.get("debit"),
                        credit=entry.get("credit"),
                    )
                )

        db_session.commit()
        db_session.refresh(transaction)

        return transaction

    return factory