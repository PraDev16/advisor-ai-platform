from sqlalchemy.orm import Session

from Backend.database.db import SessionLocal
from Backend.database.models import Client


def seed_clients():

    db: Session = SessionLocal()

    existing_clients = db.query(Client).count()

    if existing_clients == 0:

        clients = [

            Client(
                name="John Smith",
                age=45,
                risk="Moderate",
                aum="$1.2M"
            ),

            Client(
                name="Sarah Johnson",
                age=38,
                risk="Aggressive",
                aum="$2.5M"
            ),

            Client(
                name="Michael Brown",
                age=60,
                risk="Conservative",
                aum="$850K"
            )
        ]

        db.add_all(clients)

        db.commit()

    db.close()