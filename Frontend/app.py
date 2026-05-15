import streamlit as st
import requests
import plotly.express as px
import pandas as pd
import time

# Page configuration
st.set_page_config(
    page_title="Advisor AI Concierge",
    page_icon="💼",
    layout="wide"
)

# Backend API URL
BACKEND_URL = "http://backend:8000"

# -----------------------------
# SESSION STATE
# -----------------------------
if "logged_in" not in st.session_state:

    st.session_state.logged_in = False

if "token" not in st.session_state:

    st.session_state.token = None

if "role" not in st.session_state:

    st.session_state.role = None

# -----------------------------
# LOGIN SCREEN
# -----------------------------
if not st.session_state.logged_in:

    st.title("Advisor AI Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        response = requests.post(
            f"{BACKEND_URL}/login",
            json={
                "username": username,
                "password": password
            }
        )

        result = response.json()

        if result["status"] == "success":

            st.session_state.logged_in = True

            st.session_state.token = result["access_token"]

            st.session_state.role = result["role"]

            st.success(
                f"Logged in as {result['role']}"
            )

            time.sleep(1)

            st.rerun()

        else:

            st.error("Invalid credentials")

    st.stop()

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("Advisor AI")

st.sidebar.write(
    "Enterprise Financial Advisor Assistant"
)

# -----------------------------
# LOGGED-IN USER
# -----------------------------
st.sidebar.success(
    f"Logged in as: {st.session_state.role}"
)

# -----------------------------
# LOGOUT BUTTON
# -----------------------------
if st.sidebar.button("Logout"):

    st.session_state.logged_in = False

    st.session_state.token = None

    st.session_state.role = None

    st.rerun()

# -----------------------------
# ROLE-BASED NAVIGATION
# -----------------------------
if st.session_state.role == "advisor":

    pages = [
    "Advisor Chat",
    "Client 360",
    "Portfolio Insights",
    "Recommendations",
    "Analytics Dashboard",
    "Observability Dashboard"
]

elif st.session_state.role == "compliance":

    pages = [
        "Compliance Center",
        "Client 360",
        "Observability Dashboard"
    ]

else:

    pages = [
    "Advisor Chat",
    "Client 360",
    "Portfolio Insights",
    "Recommendations",
    "Analytics Dashboard",
    "Observability Dashboard"
]

page = st.sidebar.radio(
    "Navigation",
    pages
)

# -----------------------------
# TITLE
# -----------------------------
st.title("Advisor AI Concierge")

st.write("""
AI-powered intelligent assistant for financial advisors.
Provides portfolio insights, compliance monitoring,
client intelligence, and conversational AI support.
""")

# -----------------------------
# ADVISOR CHAT (RAG CONNECTED)
# -----------------------------
if page == "Advisor Chat":

    st.header("Conversational Advisor Assistant")

    # -----------------------------
    # PDF UPLOAD
    # -----------------------------
    st.subheader("Upload Research Documents")

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file,
                "application/pdf"
            )
        }

        upload_response = requests.post(
            f"{BACKEND_URL}/upload/pdf",
            files=files
        )

        upload_result = upload_response.json()

        if upload_result["status"] == "success":

            st.success(
                f"PDF ingested successfully. "
                f"Chunks added: "
                f"{upload_result['chunks_added']}"
            )

    memory_response = requests.get(
        f"{BACKEND_URL}/memory/user1"
    )

    memory_data = memory_response.json()

    history = memory_data["history"]

    for msg in history:

        with st.chat_message(msg["role"]):

            st.markdown(msg["content"])

    user_query = st.chat_input(
        "Ask your financial question..."
    )

    if user_query:

        st.chat_message("user").markdown(
            user_query
        )

        response = requests.post(
            f"{BACKEND_URL}/rag/query",
            json={
                "question": user_query,
                "session_id": "user1"
            }
        )

        data = response.json()

        ai_response = data["answer"]

        with st.chat_message("assistant"):

            st.markdown(ai_response)

# -----------------------------
# CLIENT 360
# -----------------------------
elif page == "Client 360":

    st.header("Client 360 Dashboard")

    st.write(
        "Unified wealth management client overview."
    )

    # -----------------------------
    # FETCH CLIENT LIST
    # -----------------------------
    client_response = requests.get(
        f"{BACKEND_URL}/clients"
    )

    client_names = client_response.json()["clients"]

    # -----------------------------
    # CLIENT SELECTOR
    # -----------------------------
    client_name = st.selectbox(
        "Select Client",
        client_names
    )

    # -----------------------------
    # FETCH CLIENT DATA
    # -----------------------------
    selected_client_response = requests.get(
        f"{BACKEND_URL}/clients/{client_name}"
    )

    client = selected_client_response.json()["client"]

    # -----------------------------
    # CLIENT KPIs
    # -----------------------------
    st.subheader(client_name)

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:

        st.metric(
            label="Age",
            value=client["age"]
        )

    with kpi2:

        st.metric(
            label="Risk Profile",
            value=client["risk"]
        )

    with kpi3:

        st.metric(
            label="Assets Under Management",
            value=f"${int(client['aum']):,}"
        )

    with kpi4:

        st.metric(
            label="Annual Return",
            value=f"{client['annual_return']}%"
        )

    # -----------------------------
    # INVESTMENT GOAL
    # -----------------------------
    st.subheader("Investment Goal")

    st.info(
        client["investment_goal"]
    )

    # -----------------------------
    # PORTFOLIO ALLOCATION
    # -----------------------------
    st.subheader("Portfolio Allocation")

    allocation_df = pd.DataFrame({

        "Asset Class": [
            "Equity",
            "Bonds",
            "Cash"
        ],

        "Allocation": [

            client["equity"],

            client["bonds"],

            client["cash"]
        ]
    })

    fig_client = px.pie(

        allocation_df,

        names="Asset Class",

        values="Allocation",

        title="Client Portfolio Distribution"
    )

    st.plotly_chart(
        fig_client,
        use_container_width=True
    )

    # -----------------------------
    # PORTFOLIO BREAKDOWN
    # -----------------------------
    st.subheader("Portfolio Breakdown")

    col5, col6, col7 = st.columns(3)

    with col5:

        st.metric(
            label="Equity Allocation",
            value=f"{client['equity']}%"
        )

    with col6:

        st.metric(
            label="Bond Allocation",
            value=f"{client['bonds']}%"
        )

    with col7:

        st.metric(
            label="Cash Allocation",
            value=f"{client['cash']}%"
        )

    # -----------------------------
    # AI INSIGHTS
    # -----------------------------
    st.subheader("AI Insights")

    insight_response = requests.post(

        f"{BACKEND_URL}/insights/generate",

        json={

            "client_profile":
                client["risk"].lower(),

            "equity":
                client["equity"],

            "bonds":
                client["bonds"],

            "cash":
                client["cash"]
        }
    )

    insight_result = insight_response.json()

    for item in insight_result["insights"]:

        severity = item["severity"]

        if severity == "High":

            st.error(
                f"{item['type']}: {item['message']}"
            )

        elif severity == "Medium":

            st.warning(
                f"{item['type']}: {item['message']}"
            )

        else:

            st.success(
                f"{item['type']}: {item['message']}"
            )

    # -----------------------------
    # CLIENT HEALTH SUMMARY
    # -----------------------------
    st.subheader("Client Health Summary")

    if client["risk"] == "Aggressive":

        st.warning(
            "High equity exposure detected. Portfolio may experience elevated volatility."
        )

    elif client["risk"] == "Moderate":

        st.info(
            "Balanced portfolio allocation with moderate risk exposure."
        )

    else:

        st.success(
            "Conservative allocation aligned with capital preservation strategy."
        )

# -----------------------------
# PORTFOLIO INSIGHTS
# -----------------------------
elif page == "Portfolio Insights":

    st.header("Portfolio Analytics")

    st.write(
        "Analyze portfolio risk and allocation."
    )

    equity = st.slider(
        "Equity Allocation (%)",
        0,
        100,
        60
    )

    bonds = st.slider(
        "Bond Allocation (%)",
        0,
        100,
        30
    )

    cash = st.slider(
        "Cash Allocation (%)",
        0,
        100,
        10
    )

    if st.button("Analyze Portfolio"):

        response = requests.post(
            f"{BACKEND_URL}/portfolio/analyze",
            json={
                "equity": equity,
                "bonds": bonds,
                "cash": cash
            }
        )

        result = response.json()

        st.subheader("Risk Analysis")

        st.write(
            f"### Risk Level: {result['risk_level']}"
        )

        st.write("### Portfolio Allocation")

        portfolio_data = pd.DataFrame({
            "Asset": [
                "Equity",
                "Bonds",
                "Cash"
            ],
            "Allocation": [
                result["equity"],
                result["bonds"],
                result["cash"]
            ]
        })

        fig = px.pie(
            portfolio_data,
            names="Asset",
            values="Allocation",
            title="Portfolio Allocation Breakdown"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.write("### Warnings")

        if result["warnings"]:

            for warning in result["warnings"]:

                st.warning(warning)

        else:

            st.success(
                "No major warnings detected"
            )

        st.write("### Recommendations")

        for rec in result["recommendations"]:

            st.info(rec)

# -----------------------------
# COMPLIANCE CENTER
# -----------------------------
elif page == "Compliance Center":

    st.header("Compliance Monitoring")

    st.write(
        "Validate portfolio suitability and compliance."
    )

    client_profile = st.selectbox(
        "Client Profile",
        [
            "conservative",
            "moderate",
            "aggressive",
            "retired"
        ]
    )

    equity_allocation = st.slider(
        "Equity Allocation (%)",
        0,
        100,
        60
    )

    if st.button("Run Compliance Check"):

        response = requests.post(
            f"{BACKEND_URL}/compliance/check",
            json={
                "client_profile": client_profile,
                "equity_allocation": equity_allocation
            }
        )

        result = response.json()

        st.subheader("Compliance Status")

        if result["status"] == "Compliant":

            st.success(
                "Portfolio is compliant"
            )

        else:

            st.error(
                "Portfolio is non-compliant"
            )

        st.write("### Alerts")

        if len(result["alerts"]) > 0:

            for alert in result["alerts"]:

                st.warning(alert)

        else:

            st.success(
                "No compliance alerts detected"
            )

        st.write("### Recommendations")

        for rec in result["recommendations"]:

            st.info(rec)

# -----------------------------
# ANALYTICS DASHBOARD
# -----------------------------
elif page == "Analytics Dashboard":

    st.title("Enterprise Analytics Dashboard")

    response = requests.get(
        f"{BACKEND_URL}/analytics/summary"
    )

    data = response.json()

    kpi1, kpi2, kpi3 = st.columns(3)

    with kpi1:

        st.metric(
            "Total Clients",
            data["total_clients"]
        )

    with kpi2:

        st.metric(
            "Total AUM",
            f"${data['total_aum']:,}"
        )

    with kpi3:

        st.metric(
            "Average Return",
            f"{data['avg_return']}%"
        )

    st.subheader("Risk Distribution")

    risk_df = pd.DataFrame({

        "Risk Profile":
            list(data["risk_distribution"].keys()),

        "Clients":
            list(data["risk_distribution"].values())
    })

    fig = px.pie(

        risk_df,

        names="Risk Profile",

        values="Clients",

        title="Client Risk Segmentation"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -----------------------------
# OBSERVABILITY DASHBOARD
# -----------------------------
elif page == "Observability Dashboard":

    st.header("Enterprise Observability Dashboard")

    st.write(
        "Monitor AI activity, alerts, sessions, and system metrics."
    )

    metrics_response = requests.get(
        f"{BACKEND_URL}/system/metrics"
    )

    metrics = metrics_response.json()

    # KPI METRICS
    m1, m2, m3, m4, m5 = st.columns(5)

    with m1:
        st.metric(
            "AI Queries",
            metrics["ai_queries"]
        )

    with m2:
        st.metric(
            "Compliance Alerts",
            metrics["compliance_alerts"]
        )

    with m3:
        st.metric(
            "Uploaded Docs",
            metrics["uploaded_documents"]
        )

    with m4:
        st.metric(
            "Active Sessions",
            metrics["active_sessions"]
        )

    with m5:
        st.metric(
            "Market Events",
            metrics["market_events"]
        )

    # EVENT VISUALIZATION
    st.subheader("AI Event Monitoring")

    chart_data = pd.DataFrame({
        "Category": [
            "AI Queries",
            "Compliance Alerts",
            "Uploaded Docs",
            "Market Events"
        ],
        "Count": [
            metrics["ai_queries"],
            metrics["compliance_alerts"],
            metrics["uploaded_documents"],
            metrics["market_events"]
        ]
    })

    fig = px.bar(
        chart_data,
        x="Category",
        y="Count",
        title="Enterprise AI Activity"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.success(
        "Observability systems operational."
    )

# -----------------------------
# RECOMMENDATIONS
# -----------------------------
elif page == "Recommendations":

    st.header("AI Investment Recommendations")

    st.write(
        "Generate intelligent portfolio recommendations."
    )

    client_profile = st.selectbox(
        "Client Profile",
        [
            "conservative",
            "moderate",
            "aggressive",
            "retired"
        ],
        key="recommendation_profile"
    )

    equity = st.slider(
        "Equity Allocation (%)",
        0,
        100,
        60,
        key="recommendation_equity"
    )

    bonds = st.slider(
        "Bond Allocation (%)",
        0,
        100,
        30,
        key="recommendation_bonds"
    )

    cash = st.slider(
        "Cash Allocation (%)",
        0,
        100,
        10,
        key="recommendation_cash"
    )

    if st.button("Generate Recommendations"):

        response = requests.post(
            f"{BACKEND_URL}/recommendations/generate",
            json={
                "client_profile": client_profile,
                "equity": equity,
                "bonds": bonds,
                "cash": cash
            }
        )

        result = response.json()

        st.subheader("AI Recommendations")

        for rec in result["recommendations"]:

            st.info(
                f"Recommendation: {rec['recommendation']}"
            )

            st.caption(
                f"Reason: {rec['reason']}"
            )