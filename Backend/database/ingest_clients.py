import pandas as pd

from Backend.database.db import SessionLocal
from Backend.database.models import Client


def ingest_clients():

    print("INGEST FUNCTION STARTED")

    df = pd.read_csv("/app/Backend/database/wealth_clients.csv")

    print("CSV LOADED")
    print(df.head())

    db = SessionLocal()

    existing = db.query(Client).count()

    print("EXISTING CLIENT COUNT:", existing)

    if existing == 0:

        for _, row in df.iterrows():

            client = Client(

                name=row["name"],
                age=row["age"],
                risk=row["risk"],
                aum=str(row["aum"]),
                equity=row["equity"],
                bonds=row["bonds"],
                cash=row["cash"],
                annual_return=str(row["annual_return"]),
                investment_goal=row["investment_goal"]
            )

            db.add(client)

        db.commit()

        print("CSV CLIENTS INSERTED")

    db.close()