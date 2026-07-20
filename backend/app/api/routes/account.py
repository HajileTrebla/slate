from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from sqlalchemy.orm import Session

from app.core.auth import get_current_user

from app.core.db import get_db
from app.schemas.account import AccountCreate, AccountResponse, AccountUpdate

from app.services.account_service import create_account, update_account, get_account, get_accounts, get_accounts_by_user

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"],
)


@router.post(
    "/",
    response_model=AccountResponse,
    status_code=201
)
async def create_account_route(
    payload: AccountCreate,
    db: Session=Depends(get_db),
    current_user=Depends(get_current_user),
):
    return create_account(
        db=db,
        user_id=current_user.uuid,
        payload=payload
    )


@router.get(
    "/",
    response_model=list[AccountResponse],
)
async def get_accounts_route(
    db: Session=Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_accounts(
        db=db,
    )


@router.get(
    "/my",
    response_model=list[AccountResponse],
)
async def get_account_by_user_route(
    db: Session=Depends(get_db),
    current_user=Depends(get_current_user),
):
    account = get_accounts_by_user(
        db=db,
        user_id=current_user.uuid,
    )

    if not account:
        raise HTTPException(
            status_code=404,
            detail="User has no Accounts"
        )
    
    return account


@router.get(
    "/{account_id}",
    response_model=AccountResponse,
)
async def get_account_route(
    account_id: str,
    db: Session=Depends(get_db),
    current_user=Depends(get_current_user),
):
    account = get_account(
        db=db,
        user_id=current_user.uuid,
        account_id=account_id,
    )

    if not account:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )
    
    return account
