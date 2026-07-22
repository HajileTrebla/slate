from sqlalchemy.orm import Session

from app.models.transaction_entry import TransactionEntry
from app.schemas.transaction_entry import TransactionEntryCreate, TransactionEntryUpdate


def create_transaction_entry(
        db: Session,
        transaction_id: str,
        payload: TransactionEntryCreate,
) -> TransactionEntry:
    
    entry = TransactionEntry(
        transaction_id=transaction_id,
        account_id=payload.account_id,
        debit=payload.debit,
        credit=payload.credit,
    )

    db.add(entry)
    db.commit()
    db.refresh(entry)

    return entry


def update_transaction_entry(
        db: Session,
        entry_id: str,
        payload: TransactionEntryUpdate
) -> TransactionEntry:

    entry = (
        db.query(TransactionEntry)
        .filter(TransactionEntry.uuid == entry_id)
        .first()
    )

    if payload.account_id is not None:
        entry.account_id = payload.account_id
    if payload.credit is not None:
        entry.credit = payload.credit
    if payload.debit is not None:
        entry.debit = payload.debit

    db.commit()
    db.refresh(entry)

    return entry


def get_transaction_entry(
        db: Session,
        entry_id: str,
        transaction_id: str,
) -> TransactionEntry:

    return(
        db.query(TransactionEntry)
        .filter(
                TransactionEntry.uuid == entry_id,
                TransactionEntry.transaction_id == transaction_id,
            )
        .first()
    )


def get_transaction_entries(
        db: Session,
        transaction_id: str,
) -> TransactionEntry:

    return(
        db.query(TransactionEntry)
        .filter(TransactionEntry.transaction_id == transaction_id)
        .all()
    )
