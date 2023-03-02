from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.orm import Session
from db.models import Client, BankAccount


def get_clients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Client).offset(skip).limit(limit).all()


def get_balance_by_id(db: Session, client_id: int):
    return db.query(BankAccount).filter(BankAccount.client_id == client_id).first()


def add_money(db: Session, client_id: int, money: int):
    client = db.query(BankAccount).filter(
        BankAccount.client_id == client_id).first()
    db.execute(update(BankAccount).where(BankAccount.client_id == client_id).values(
        client_money=client.client_money + money))
    db.commit()
    return client


def buy_for_money(db: Session, client_id: int, money: int):
    client = db.query(BankAccount).filter(
        BankAccount.client_id == client_id).first()
    if (client.client_money-money) < 0:
        raise HTTPException(
            status_code=404, detail="У вас не хватит на это денег")
    db.execute(update(BankAccount).where(BankAccount.client_id == client_id).values(
        client_money=client.client_money - money))
    db.commit()
    return client
