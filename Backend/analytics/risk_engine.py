def analyze_portfolio(equity, bonds, cash):

    risk_level = "Moderate"

    warnings = []

    recommendations = []

    # -----------------------------
    # RISK CLASSIFICATION
    # -----------------------------
    if equity >= 80:

        risk_level = "High"

        warnings.append(
            "Equity exposure exceeds 80%"
        )

        recommendations.append(
            "Reduce equity allocation"
        )

    elif equity <= 40:

        risk_level = "Low"

        recommendations.append(
            "Portfolio is conservatively positioned"
        )

    else:

        risk_level = "Moderate"

        recommendations.append(
            "Maintain diversified allocation strategy"
        )

    # -----------------------------
    # DIVERSIFICATION CHECK
    # -----------------------------
    if bonds < 20:

        warnings.append(
            "Low fixed income exposure"
        )

        recommendations.append(
            "Increase bond allocation for stability"
        )

    # -----------------------------
    # CASH POSITION CHECK
    # -----------------------------
    if cash < 5:

        warnings.append(
            "Low liquidity position"
        )

        recommendations.append(
            "Maintain higher cash reserves"
        )

    # -----------------------------
    # DEFAULT RECOMMENDATION
    # -----------------------------
    if len(recommendations) == 0:

        recommendations.append(
            "Portfolio allocation appears balanced"
        )

    # -----------------------------
    # FINAL RESPONSE
    # -----------------------------
    return {
        "risk_level": risk_level,
        "equity": equity,
        "bonds": bonds,
        "cash": cash,
        "warnings": warnings,
        "recommendations": recommendations
    }