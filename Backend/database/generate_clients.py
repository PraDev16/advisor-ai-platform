import random
import pandas as pd
from faker import Faker

fake = Faker()

risk_profiles = [
    "Conservative",
    "Moderate",
    "Aggressive"
]

investment_goals = [
    "Retirement Planning",
    "Wealth Expansion",
    "Passive Income",
    "Education Planning",
    "Capital Appreciation",
    "Balanced Income",
    "Long-Term Growth",
    "Portfolio Diversification"
]

clients = []

for _ in range(1000):

    risk = random.choice(risk_profiles)

    if risk == "Conservative":
        equity = random.randint(20, 40)
        bonds = random.randint(40, 60)

    elif risk == "Moderate":
        equity = random.randint(50, 70)
        bonds = random.randint(20, 40)

    else:
        equity = random.randint(75, 95)
        bonds = random.randint(5, 20)

    cash = 100 - (equity + bonds)

    client = {

        "name": fake.name(),

        "age": random.randint(25, 75),

        "risk": risk,

        "aum": random.randint(100000, 5000000),

        "equity": equity,

        "bonds": bonds,

        "cash": cash,

        "annual_return": round(random.uniform(4, 18), 2),

        "investment_goal": random.choice(investment_goals)
    }

    clients.append(client)

df = pd.DataFrame(clients)

df.to_csv(
    "Backend/database/wealth_clients.csv",
    index=False
)

print("1000 client dataset generated successfully.")