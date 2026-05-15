def generate_insights(
    client_profile,
    equity,
    bonds,
    cash
):

    insights = []

    # -----------------------------
    # HIGH EQUITY RISK
    # -----------------------------
    if equity >= 80:

        insights.append({
            "type": "Risk Alert",
            "message":
            "Portfolio equity exposure is significantly high.",
            "severity": "High"
        })

    # -----------------------------
    # LOW BOND EXPOSURE
    # -----------------------------
    if bonds < 20:

        insights.append({
            "type": "Diversification Alert",
            "message":
            "Fixed income allocation may be insufficient for stability.",
            "severity": "Medium"
        })

    # -----------------------------
    # LOW CASH POSITION
    # -----------------------------
    if cash < 5:

        insights.append({
            "type": "Liquidity Alert",
            "message":
            "Low liquidity reserves detected in portfolio.",
            "severity": "Medium"
        })

    # -----------------------------
    # RETIRED CLIENT CHECK
    # -----------------------------
    if (
        client_profile == "retired"
        and equity > 50
    ):

        insights.append({
            "type": "Retirement Risk",
            "message":
            "Retired client may face elevated market volatility exposure.",
            "severity": "High"
        })

    # -----------------------------
    # CONSERVATIVE CLIENT CHECK
    # -----------------------------
    if (
        client_profile == "conservative"
        and equity > 60
    ):

        insights.append({
            "type": "Suitability Alert",
            "message":
            "Portfolio allocation may not align with conservative objectives.",
            "severity": "High"
        })

    # -----------------------------
    # DEFAULT
    # -----------------------------
    if len(insights) == 0:

        insights.append({
            "type": "Portfolio Health",
            "message":
            "Portfolio allocation appears healthy and aligned.",
            "severity": "Low"
        })

    return {
        "client_profile": client_profile,
        "insights": insights
    }