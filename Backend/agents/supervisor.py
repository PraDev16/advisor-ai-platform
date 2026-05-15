from Backend.rag.rag_engine import ask_rag

from Backend.compliance.compliance_checker import (
    check_compliance
)

from Backend.analytics.risk_engine import (
    analyze_portfolio
)

from Backend.recommendation.recommendation_engine import (
    generate_recommendations
)

# -----------------------------
# SUPERVISOR AGENT
# -----------------------------
def route_query(query):

    query_lower = query.lower()

    # -----------------------------
    # COMPLIANCE AGENT
    # -----------------------------
    if (
        "compliance" in query_lower
        or "retired" in query_lower
        or "risk violation" in query_lower
    ):

        result = check_compliance(
            "retired",
            85
        )

        return {
            "agent": "Compliance Agent",
            "response": result
        }

    # -----------------------------
    # PORTFOLIO AGENT
    # -----------------------------
    elif (
        "portfolio" in query_lower
        or "allocation" in query_lower
        or "diversification" in query_lower
    ):

        result = analyze_portfolio(
            70,
            20,
            10
        )

        return {
            "agent": "Portfolio Agent",
            "response": result
        }

    # -----------------------------
    # RECOMMENDATION AGENT
    # -----------------------------
    elif (
        "recommend" in query_lower
        or "investment advice" in query_lower
        or "next best action" in query_lower
    ):

        result = generate_recommendations(
            "moderate",
            70,
            20,
            10
        )

        return {
            "agent": "Recommendation Agent",
            "response": result
        }

    # -----------------------------
    # RESEARCH / RAG AGENT
    # -----------------------------
    else:

        result = ask_rag(query)

        return {
            "agent": "Research Agent",
            "response": result
        }