from Backend.database.db import SessionLocal
from Backend.database.models import Client


def get_all_clients():

    db = SessionLocal()

    clients = db.query(Client).all()

    client_names = [client.name for client in clients]

    db.close()

    return client_names


def get_client(client_name: str):

    db = SessionLocal()

    client = (
        db.query(Client)
        .filter(Client.name == client_name)
        .first()
    )

    db.close()

    if not client:

        return None

    return {

        "name": client.name,

        "age": client.age,

        "risk": client.risk,

        "aum": client.aum,

        "equity": client.equity,

        "bonds": client.bonds,

        "cash": client.cash,

        "annual_return": client.annual_return,

        "investment_goal": client.investment_goal
    }