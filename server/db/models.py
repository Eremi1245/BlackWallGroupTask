from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import MONEY
from sqlalchemy.orm import relationship
from .database import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(200), nullable=False)
    last_name = Column(String(200), nullable=False)

    bank_account = relationship("BankAccount", back_populates="client")


class BankAccount(Base):
    __tablename__ = 'clients_bank_account'

    bank_account = Column(Integer, primary_key=True)
    client_id = Column(ForeignKey(
        'clients.id'))
    client_money = Column(Integer)

    client = relationship("Client", back_populates="bank_account")
