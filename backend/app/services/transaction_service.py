from sqlalchemy.orm import Session
from datetime import datetime

from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate


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

    db.commit()
    db.refresh(transaction)

    return transaction


def get_transaction(
        db: Session,
        transaction_id: str,
) -> Transaction | None:
    
    return (
        db.query(Transaction)
        .filter(Transaction.uuid == transaction_id)
        .first()
    )


def get_transactions(
        db: Session,
) -> Transaction | None:
    
    return (
        db.query(Transaction)
        .all()
    )
