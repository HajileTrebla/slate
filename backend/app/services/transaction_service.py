from sqlalchemy.orm import Session

from app.models.transaction import Transaction

from app.schemas.transaction import (
    TransactionCreate,
    TransactionUpdate,
)

from app.schemas.transaction_entry import (
    TransactionEntryCreate,
)


def _create_entries(
    transaction: Transaction,
    entries: list[TransactionEntryCreate]
):

    if entries is None:
        return

    for entry in entries:
        transaction.entries.append(
            account_id= entry.account_id,
            debit= entry.debit,
            credit= entry.credit,
        )


def _replace_entries(
    transaction: Transaction,
    entries: list[TransactionEntryCreate]
) -> None:

    transaction.entries.clear()

    _create_entries(
        transaction=transaction,
        entries=entries,
    )


def create_transaction(
        db: Session,
        payload: TransactionCreate,
) -> Transaction:
    
    transaction = Transaction(
        date= payload.date,
        description= payload.description,
        reference= payload.reference,
    )

    db.add(transaction)

    _create_entries(
        transaction=transaction,
        entries=payload.entries
    )

    db.commit()
    db.refresh(transaction)

    return transaction


def update_transaction(
        db: Session,
        transaction_id: str,
        payload: TransactionUpdate,
) -> Transaction:
    
    transaction = (
        db.query(Transaction)
        .filter(Transaction.uuid == transaction_id)
        .first()
    )

    if payload.date is not None:
        transaction.date = payload.date

    if payload.description is not None:
        transaction.description = payload.description

    if payload.reference is not None:
        transaction.reference = payload.reference

    if payload.entries is not None:

        _replace_entries(
            transaction=transaction,
            entries=payload.entries
        )


    db.commit()
    db.refresh(transaction)

    return transaction


def get_transaction(
        db: Session,
        transaction_id: str,
) -> Transaction | None:
    
    transaction = (
        db.query(Transaction)
        .filter(Transaction.uuid == transaction_id)
        .first()
    )

    return transaction


def get_transactions(
        db: Session,
) -> Transaction | None:
    
    return (
        db.query(Transaction)
        .all()
    )
