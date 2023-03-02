import json
from fastapi import APIRouter, Depends, HTTPException
from api.operations import clients as _clients_operations
from db.schemas import Client, Balance, BankAccount
from db.dependencies import get_db
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
router = APIRouter(
    prefix="/clients",
    tags=["clients"],
    # dependencies=[Depends(_users_actions.get_current_user)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[Client])
def get_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clients = _clients_operations.get_clients(db, skip=skip, limit=limit)
    return clients


# Возвращает баланс клиента
@router.get("/{client_id}", response_model=Balance)
def get_balance_by_id(client_id: int, db: Session = Depends(get_db)):
    client_balance = _clients_operations.get_balance_by_id(
        db, client_id=client_id)
    if client_balance is None:
        raise HTTPException(status_code=404, detail="User not found")
    return client_balance


# Обновляет балас клиента
@router.put("/{operation}/{client_id}", response_model=Balance)
def update_client(client_id: str, operation: str, value: int, db: Session = Depends(get_db)):
    if operation == "add":
        result = _clients_operations.add_money(db,
                                               client_id=client_id, money=value)
    elif operation == "buy":
        result = _clients_operations.buy_for_money(db,
                                                   client_id=client_id, money=value)
    return result
