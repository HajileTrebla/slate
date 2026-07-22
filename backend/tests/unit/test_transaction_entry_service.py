import pytest

from datetime import datetime, UTC

from app.services.user_service import create_user
from app.services.account_service import create_account
from app.services.transaction_service import create_transaction
from app.services.transaction_entry_service import create_transaction_entry, update_transaction_entry, get_transaction_entries, get_transaction_entry

from app.schemas.user import UserCreate
from app.schemas.account import AccountCreate
from app.schemas.transaction import TransactionCreate
from app.schemas.transaction_entry import TransactionEntryCreate, TransactionEntryUpdate


@pytest.fixture
def entry_context(db_session):

    user = create_user(
        db=db_session,
        payload=UserCreate(
            username="entry_user",
            email="entry@test.com",
            password="password123",
        ),
    )

    # Create account
    asset = create_account(
        db=db_session,
        user_id=user.uuid,
        payload=AccountCreate(
            name="Cash",
            account_type="asset",
            currency="PHP",
        ),
    )

    expense = create_account(
        db=db_session,
        user_id=user.uuid,
        payload=AccountCreate(
            name="House Bills",
            account_type="expense",
            currency="PHP",
        ),
    )

    # Create transaction
    transaction = create_transaction(
        db=db_session,
        payload=TransactionCreate(
            date=datetime.now(UTC),
            description="Bills Payment",
            reference="BI-001-T",
        ),
    )

    return {
        "user": user,
        "asset": asset,
        "expense": expense,
        "transaction": transaction,
    }


@pytest.mark.unit
def test_create_transaction_entry(db_session, entry_context):

    asset = entry_context["asset"]
    expense = entry_context["expense"]
    transaction = entry_context["transaction"]

    payloads = [
        TransactionEntryCreate(
            account_id= asset.uuid,
            credit= 500.00
        ),
        TransactionEntryCreate(
            account_id= expense.uuid,
            debit= 500.00
        ),
    ]

    entries: list = []

    for payload in payloads:
        entries.append(
            create_transaction_entry(
                db=db_session,
                transaction_id=transaction.uuid,
                payload=payload,
            )
        )

    assert entries is not None
    assert len(entries) == 2
    assert entries[0].account_id == asset.uuid
    assert entries[1].account_id == expense.uuid


@pytest.mark.unit
def test_update_transaction_entry(db_session, entry_context):

    asset = entry_context["asset"]
    expense = entry_context["expense"]
    transaction = entry_context["transaction"]

    create_payloads = [
        TransactionEntryCreate(
            account_id= asset.uuid,
            credit= 500.00
        ),
        TransactionEntryCreate(
            account_id= expense.uuid,
            debit= 500.00
        ),
    ]

    old_entries: list = []

    for payload in create_payloads:
        old_entries.append(
            create_transaction_entry(
                db=db_session,
                transaction_id=transaction.uuid,
                payload=payload,
            )
        )

    update_payloads = [
        TransactionEntryUpdate(
            credit= 1000
        ),
        TransactionEntryUpdate(
            debit= 1000
        )
    ] 

    entries: list = []

    for i in range(len(update_payloads)):
        entries.append(
            update_transaction_entry(
                db=db_session,
                entry_id=old_entries[i].uuid,
                payload=update_payloads[i]
            )
        )
        

    assert entries is not None
    assert len(entries) == 2
    assert entries[0].credit == 1000
    assert entries[1].debit == 1000


@pytest.mark.unit
def test_get_transaction_entry(db_session, entry_context):

    asset = entry_context["asset"]
    expense = entry_context["expense"]
    transaction = entry_context["transaction"]

    payloads = [
        TransactionEntryCreate(
            account_id= asset.uuid,
            credit= 500.00
        ),
        TransactionEntryCreate(
            account_id= expense.uuid,
            debit= 500.00
        ),
    ]

    entries: list = []

    for payload in payloads:
        entries.append(
            create_transaction_entry(
                db=db_session,
                transaction_id=transaction.uuid,
                payload=payload,
            )
        )

    entry = get_transaction_entry(
        db= db_session,
        entry_id= entries[0].uuid,
        transaction_id= transaction.uuid
    )

    assert entry is not None
    assert entry.debit == 0
    assert entry.credit == 500


@pytest.mark.unit
def test_get_transaction_entries(db_session, entry_context):

    asset = entry_context["asset"]
    expense = entry_context["expense"]
    transaction = entry_context["transaction"]

    payloads = [
        TransactionEntryCreate(
            account_id= asset.uuid,
            credit= 500.00
        ),
        TransactionEntryCreate(
            account_id= expense.uuid,
            debit= 500.00
        ),
    ]

    entries: list = []

    for payload in payloads:
        entries.append(
            create_transaction_entry(
                db=db_session,
                transaction_id=transaction.uuid,
                payload=payload,
            )
        )

    entries = get_transaction_entries(
        db= db_session,
        transaction_id= transaction.uuid
    )

    assert entries is not None
    assert len(entries) == 2
