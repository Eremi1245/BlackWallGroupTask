from pydantic import BaseModel
from typing import List


class BankAccount(BaseModel):
    bank_account: str
    client_money: int

    class Config:
        orm_mode = True


class Client(BaseModel):
    id: int
    first_name: str
    last_name: str

    bank_account: List[BankAccount]

    class Config:
        orm_mode = True


class Balance(BaseModel):
    client_money: int = 0

    class Config:
        orm_mode = True
