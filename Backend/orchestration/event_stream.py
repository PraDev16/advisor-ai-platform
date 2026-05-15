import random
from datetime import datetime

# -----------------------------
# MARKET EVENTS
# -----------------------------
market_events = [
    {
        "event": "Tech sector volatility spike",
        "severity": "High"
    },
    {
        "event": "Bond market stability increase",
        "severity": "Low"
    },
    {
        "event": "Liquidity risk detected",
        "severity": "High"
    },
    {
        "event": "Energy sector outperforming",
        "severity": "Medium"
    },
    {
        "event": "Large-cap equities declining",
        "severity": "Medium"
    }
]

# -----------------------------
# EVENT GENERATOR
# -----------------------------
def generate_market_event():

    event = random.choice(market_events)

    return {
        "timestamp": str(datetime.now()),
        "event": event["event"],
        "severity": event["severity"]
    }