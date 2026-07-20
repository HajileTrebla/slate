from sqlalchemy.orm import Session

from app.models.account import Account
from app.schemas.account import AccountCreate, AccountUpdate


def create_account(
    db: Session,
    user_id: str,
    payload: AccountCreate,
) -> Account:

    account = Account(
        user_id=user_id,
        name=payload.name,
        account_type=payload.account_type,
        currency=payload.currency,
    )

    db.add(account)
    db.commit()
    db.refresh(account)

    return account


def update_account(
    db: Session,
    user_id: str,
    payload: AccountUpdate,
) -> Account:

    account = (
        db.query(Account)
        .filter(
            Account.uuid == payload.uuid,
            Account.user_id == user_id
        )
        .first()
    )

    if payload.name is not None:
        account.name = payload.name

    if payload.account_type is not None:
        account.account_type = payload.account_type

    if payload.currency is not None:
        account.currency = payload.currency

    if payload.is_archived is not None:
        account.is_archived = payload.is_archived

    db.commit()
    db.refresh(account)

    return account


def get_account(
    db: Session,
    user_id: str,
    account_id: str,
) -> Account | None:

    return (
        db.query(Account)
        .filter(
            Account.uuid == account_id,
            Account.user_id == user_id,    
        )
        .first()
    )


def get_accounts(
    db: Session,
) -> list[Account]:

    return db.query(Account).all()


def get_accounts_by_user(
    db: Session,
    user_id: str,
) -> list[Account]:

    return (
        db.query(Account)
        .filter(Account.user_id == user_id)
        .all()
    )
