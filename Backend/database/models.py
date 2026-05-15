from sqlalchemy import Column, Integer, String
from Backend.database.db import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True, index=True)

    password = Column(String)

    role = Column(String)


class Client(Base):

    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)

    age = Column(Integer)

    risk = Column(String)

    aum = Column(String)

    equity = Column(Integer)

    bonds = Column(Integer)

    cash = Column(Integer)

    annual_return = Column(String)

    investment_goal = Column(String)

__all__ = ["Base", "User", "Client"]