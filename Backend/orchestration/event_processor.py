# -----------------------------
# EVENT PROCESSOR
# -----------------------------
def process_market_event(event):

    event_name = event["event"]

    alerts = []

    # -----------------------------
    # TECH VOLATILITY
    # -----------------------------
    if "Tech sector volatility" in event_name:

        alerts.append({
            "type": "Portfolio Risk",
            "severity": "High",
            "message":
            "High tech exposure portfolios should be reviewed immediately."
        })

    # -----------------------------
    # LIQUIDITY RISK
    # -----------------------------
    elif "Liquidity risk" in event_name:

        alerts.append({
            "type": "Liquidity Alert",
            "severity": "High",
            "message":
            "Clients with low cash reserves may face liquidity stress."
        })

    # -----------------------------
    # LARGE CAP DECLINE
    # -----------------------------
    elif "Large-cap equities declining" in event_name:

        alerts.append({
            "type": "Market Movement",
            "severity": "Medium",
            "message":
            "Large-cap exposure should be monitored for downside protection."
        })

    # -----------------------------
    # ENERGY SECTOR
    # -----------------------------
    elif "Energy sector outperforming" in event_name:

        alerts.append({
            "type": "Opportunity Detection",
            "severity": "Low",
            "message":
            "Energy-focused investment opportunities identified."
        })

    # -----------------------------
    # BOND STABILITY
    # -----------------------------
    elif "Bond market stability" in event_name:

        alerts.append({
            "type": "Defensive Allocation",
            "severity": "Low",
            "message":
            "Bond-heavy portfolios may benefit from current market stability."
        })

    return alerts