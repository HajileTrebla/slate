from pydantic import NonNegativeFloat
import pytest

from datetime import datetime, UTC

from app.services.transaction_service import create_transaction, update_transaction, get_transaction, get_transactions
from app.schemas.transaction import TransactionCreate, TransactionUpdate

@pytest.mark.unit
def test_create_transaction(db_session):

    payload = TransactionCreate(
        date=datetime.now(UTC),
        description="June 2026 Week 1 Grocery",
        reference="r34678-341-56426"
    )

    transaction = create_transaction(
        db=db_session,
        payload=payload,
    )

    assert transaction is not None
    assert transaction.date == payload.date
    assert transaction.description == "June 2026 Week 1 Grocery"
    assert transaction.reference == "r34678-341-56426"


@pytest.mark.unit
def test_update_transaction(db_session):

    create_payload = TransactionCreate(
        date=datetime.now(UTC),
        description="June 2026 Week 1 Grocery",
        reference="r34678-341-56426"
    )

    transaction = create_transaction(
        db=db_session,
        payload=create_payload,
    )

    update_payload = TransactionUpdate(
        description="June 2026 Week 2 Grocery"
    )

    updated_transaction = update_transaction(
        db=db_session,
        transaction_id=transaction.uuid,
        payload=update_payload,
    )

    assert updated_transaction is not None 
    assert updated_transaction.description == "June 2026 Week 2 Grocery"


@pytest.mark.unit
def test_get_transaction(db_session):

    create_payloads = [
        TransactionCreate(
            date=datetime.now(UTC),
            description="June 2026 Week 1 Grocery",
            reference="r34678-341-56426"
        ),
        TransactionCreate(
            date=datetime.now(UTC),
            description="June 2026 Week 2 Grocery",
            reference="r34678-341-56856"
        ),
    ]

    transactions: list = []
    for payload in create_payloads:
        transaction = create_transaction(
            db=db_session,
            payload=payload,
        )
        transactions.append(transaction)

    transaction = get_transaction(
        db=db_session,
        transaction_id=transactions[0].uuid
    )

    assert transaction is not None

    assert transaction is not None


@pytest.mark.unit
def test_get_transactions(db_session):

    create_payloads = [
        TransactionCreate(
            date=datetime.now(UTC),
            description="June 2026 Week 1 Grocery",
            reference="r34678-341-56426"
        ),
        TransactionCreate(
            date=datetime.now(UTC),
            description="June 2026 Week 2 Grocery",
            reference="r34678-341-56856"
        ),
    ]

    transactions: list = []
    for payload in create_payloads:
        transaction = create_transaction(
            db=db_session,
            payload=payload,
        )
        transactions.append(transaction)

    transaction = get_transactions(
        db=db_session,
    )

    assert transaction is not None
    assert len(transaction) == 2
