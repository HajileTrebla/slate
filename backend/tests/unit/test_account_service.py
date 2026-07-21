import pytest

from uuid import uuid4
from sqlalchemy.exc import IntegrityError

from app.schemas.account import AccountCreate, AccountUpdate
from app.schemas.user import UserCreate

from app.services.account_service import create_account, update_account, get_account, get_accounts, get_accounts_by_user
from app.services.user_service import create_user


@pytest.mark.unit
def test_create_account(db_session):

    user_payload = UserCreate(
            username="j.do",
            email="johndoe@gmail.com",
            password="password123",
    )

    user = create_user(
        db=db_session,
        payload=user_payload,
    )

    assert user.uuid is not None

    account_payload = AccountCreate(
            name="John Doe Savings Account",
            account_type="asset",
            currency="USD",
    )

    account = create_account(
        db=db_session,
        user_id=user.uuid,
        payload=account_payload,
    )

    assert account.uuid is not None
    assert account.user_id == user.uuid
    assert account.name == "John Doe Savings Account"
    assert account.account_type == "asset"
    assert account.currency == "USD"


@pytest.mark.unit
def test_update_account(db_session):

    user_payload = UserCreate(
            username="j.do",
            email="johndoe@gmail.com",
            password="password123",
    )

    user = create_user(
        db=db_session,
        payload=user_payload,
    )

    account_payload = AccountCreate(
            name="John Doe Savings Account",
            account_type="asset",
            currency="USD",
    )

    account = create_account(
        db=db_session,
        user_id=user.uuid,
        payload=account_payload,
    )

    # Test updating the account
    updated_account = update_account(
        db=db_session,
        account_id=account.uuid,
        user_id=user.uuid,
        payload=AccountUpdate(
            name="John Doe Auto Loan",
            account_type="liability",
            currency="EUR"
        )
    )

    assert updated_account.uuid == account.uuid
    assert updated_account.user_id == user.uuid
    assert updated_account.name == "John Doe Auto Loan"
    assert updated_account.account_type == "liability"
    assert updated_account.currency == "EUR"


@pytest.mark.unit
def test_get_account(db_session):

    user_payload = UserCreate(
            username="j.do",
            email="johndoe@gmail.com",
            password="password123",
    )

    user = create_user(
        db=db_session,
        payload=user_payload,
    )

    account_payload = AccountCreate(
            name="John Doe Savings Account",
            account_type="asset",
            currency="USD",
    )

    account = create_account(
        db=db_session,
        user_id=user.uuid,
        payload=account_payload,
    )

    retrieved_account = get_account(
        db=db_session,
        user_id=user.uuid,
        account_id=account.uuid
    )

    assert retrieved_account.uuid == account.uuid
    assert retrieved_account.user_id == user.uuid
    assert retrieved_account.name == "John Doe Savings Account"
    assert retrieved_account.account_type == "asset"
    assert retrieved_account.currency == "USD"


@pytest.mark.unit
def test_get_accounts(db_session):

    user_payload = UserCreate(
            username="j.do",
            email="johndoe@gmail.com",
            password="password123",
    )

    user = create_user(
        db=db_session,
        payload=user_payload,
    )

    account_payloads = [
        AccountCreate(
            name="John Doe Savings Account",
            account_type="asset",
            currency="USD",
        ),
        AccountCreate(
            name="John Doe Checking Account",
            account_type="asset",
            currency="USD",
        ),
    ]

    for payload in account_payloads:
        create_account(
            db=db_session,
            user_id=user.uuid,
            payload=payload,
        )

    retrieved_accounts = get_accounts(
        db=db_session,
    )

    assert len(retrieved_accounts) == 2
    assert retrieved_accounts[1].user_id == user.uuid
    assert retrieved_accounts[1].name == "John Doe Checking Account"
    assert retrieved_accounts[1].account_type == "asset"
    assert retrieved_accounts[1].currency == "USD"


@pytest.mark.unit
def test_get_accounts_by_user(db_session):

    user_payloads = [
        UserCreate(
            username="j.do",
            email="johndoe@gmail.com",
            password="password123",
        ),
        UserCreate(
            username="jane.doe",
            email="janedoe@gmail.com",
            password="password123",
        )
    ]

    users = []
    for payload in user_payloads:
        user = create_user(db=db_session, payload=payload)
        users.append(user)

    account_payloads = [
        [
            users[0].uuid,
            AccountCreate(
                name="John Doe Savings Account",
                account_type="asset",
                currency="USD",
            ),
        ],
        [
            users[1].uuid,
            AccountCreate(
                name="Jane Doe Checking Account",
                account_type="asset",
                currency="USD",
            ),
        ],
    ]

    for payload in account_payloads:
        create_account(
            db=db_session,
            user_id=payload[0],
            payload=payload[1],
        )

    retrieved_accounts = get_accounts_by_user(
        db=db_session,
        user_id=users[0].uuid
    )

    assert len(retrieved_accounts) == 1
    assert retrieved_accounts[0].user_id == users[0].uuid
    assert retrieved_accounts[0].name == "John Doe Savings Account"
    assert retrieved_accounts[0].account_type == "asset"
    assert retrieved_accounts[0].currency == "USD"


@pytest.mark.unit
def test_create_account_with_nonexistent_user(db_session):

    account_payload = AccountCreate(
            name="Non-existent User Account",
            account_type="asset",
            currency="USD",
    )

    with pytest.raises(IntegrityError, match="violates foreign key constraint"): 
        create_account(
            db=db_session,
            user_id=uuid4(),  # Non-existent user ID
            payload=account_payload,
        )
    
