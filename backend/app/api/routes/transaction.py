from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.core.auth import get_current_user

from app.core.db import get_db
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponse

from app.services.transaction_service import create_transaction, update_transaction, get_transaction, get_transactions

router = APIRouter(
    prefix="/transactions",
    tags=['Transactions']
)


@router.post(
    "/",
    response_model=TransactionResponse,
    status_code=201
)
async def create_transaction_route(
    payload: TransactionCreate,
    db: Session=Depends(get_db),
    current_user=Depends(get_current_user),
):
    return create_transaction(
        db=db,
        payload=payload,
    )


@router.get(
    "/",
    response_model=list[TransactionResponse],
)
async def get_transactions_route(
    db: Session=Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_transactions(
        db=db,
    )


@router.patch(
    "/{transaction_id}",
    response_model=TransactionResponse,
)
async def update_transaction_route(
    payload: TransactionUpdate,
    transaction_id: str,
    db: Session=Depends(get_db),
    current_user=Depends(get_current_user),
):
    return update_transaction(
        db=db,
        transaction_id=transaction_id,
        payload=payload,
    )


@router.get(
    "/{transaction_id}",
    response_model=TransactionResponse,
)
async def get_transaction_route(
    transaction_id: str,
    db: Session=Depends(get_db),
    current_user=Depends(get_current_user),
):
    transaction = get_transaction(
        db=db,
        transaction_id=transaction_id,
    )

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return transaction
