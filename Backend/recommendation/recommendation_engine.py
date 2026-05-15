def generate_recommendations(
    client_profile,
    equity,
    bonds,
    cash
):

    recommendations = []

    # -----------------------------
    # CONSERVATIVE CLIENT
    # -----------------------------
    if client_profile == "conservative":

        if equity > 60:

            recommendations.append({
                "recommendation":
                "Reduce equity exposure for lower volatility.",

                "reason":
                "Client risk profile is conservative and equity allocation exceeds 60%."
            })

        if bonds < 30:

            recommendations.append({
                "recommendation":
                "Increase bond allocation for stability.",

                "reason":
                "Bond exposure is below recommended defensive allocation."
            })

    # -----------------------------
    # RETIRED CLIENT
    # -----------------------------
    if client_profile == "retired":

        recommendations.append({
            "recommendation":
            "Focus on income-generating investments.",

            "reason":
            "Retired clients typically prioritize stable income and capital preservation."
        })

        if equity > 50:

            recommendations.append({
                "recommendation":
                "Lower equity exposure to preserve capital.",

                "reason":
                "High equity allocation may expose retired clients to excess volatility."
            })

    # -----------------------------
    # AGGRESSIVE CLIENT
    # -----------------------------
    if client_profile == "aggressive":

        recommendations.append({
            "recommendation":
            "Consider growth-oriented equity investments.",

            "reason":
            "Aggressive investors generally seek higher long-term growth potential."
        })

    # -----------------------------
    # LOW CASH CHECK
    # -----------------------------
    if cash < 5:

        recommendations.append({
            "recommendation":
            "Maintain higher liquidity reserves.",

            "reason":
            "Low cash reserves may reduce portfolio flexibility during volatility."
        })

    # -----------------------------
    # DIVERSIFICATION
    # -----------------------------
    if equity > 70 and bonds < 20:

        recommendations.append({
            "recommendation":
            "Portfolio may be under-diversified.",

            "reason":
            "High equity concentration with low fixed income increases risk exposure."
        })

    # -----------------------------
    # DEFAULT
    # -----------------------------
    if len(recommendations) == 0:

        recommendations.append({
            "recommendation":
            "Portfolio allocation appears balanced.",

            "reason":
            "Current allocation aligns with the selected client profile."
        })

    return {
        "client_profile": client_profile,
        "recommendations": recommendations
    }