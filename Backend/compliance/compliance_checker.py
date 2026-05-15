def check_compliance(client_profile, equity_allocation):

    alerts = []

    recommendations = []

    # -----------------------------
    # CONSERVATIVE CLIENT CHECK
    # -----------------------------
    if (
        client_profile.lower() == "conservative"
        and equity_allocation > 60
    ):

        alerts.append(
            "Conservative client exceeds recommended equity exposure."
        )

        recommendations.append(
            "Reduce equity allocation below 60%."
        )

    # -----------------------------
    # RETIRED CLIENT CHECK
    # -----------------------------
    if (
        client_profile.lower() == "retired"
        and equity_allocation > 50
    ):

        alerts.append(
            "Retired client may face excessive market risk."
        )

        recommendations.append(
            "Increase fixed income allocation."
        )

    # -----------------------------
    # HIGH RISK CHECK
    # -----------------------------
    if equity_allocation >= 80:

        alerts.append(
            "Portfolio classified as high risk."
        )

        recommendations.append(
            "Perform suitability review."
        )

    # -----------------------------
    # FINAL STATUS
    # -----------------------------
    status = "Compliant"

    if len(alerts) > 0:

        status = "Non-Compliant"

    # -----------------------------
    # DEFAULT RECOMMENDATION
    # -----------------------------
    if len(recommendations) == 0:

        recommendations.append(
            "Portfolio allocation aligns with compliance guidelines."
        )

    # -----------------------------
    # FINAL RESPONSE
    # -----------------------------
    return {
        "status": status,
        "client_profile": client_profile,
        "equity_allocation": equity_allocation,
        "alerts": alerts,
        "recommendations": recommendations
    }