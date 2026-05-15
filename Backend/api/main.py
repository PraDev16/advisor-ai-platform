from Backend.services.llm_service import generate_ai_response
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Backend.rag.rag_engine import ask_rag
from Backend.memory.chat_memory import get_history
from Backend.analytics.risk_engine import analyze_portfolio
from Backend.compliance.compliance_checker import check_compliance
from Backend.recommendation.recommendation_engine import generate_recommendations
from Backend.agents.insight_generator import generate_insights
from Backend.database.client_data import (
    get_all_clients,
    get_client
)
from Backend.auth.auth_handler import (
    authenticate_user,
    create_access_token
)
from Backend.knowledge_graph.graph_engine import (
    get_client_relationships
)
from Backend.agents.supervisor import route_query
from Backend.orchestration.event_stream import (
    generate_market_event
)
from Backend.orchestration.event_stream import (
    generate_market_event
)

from Backend.orchestration.event_processor import (
    process_market_event
)
from Backend.rag.pdf_ingestion import ingest_pdf
from Backend.database.db import engine
from Backend.database.models import Base
from Backend.database.seed_data import seed_clients
from Backend.database.ingest_clients import ingest_clients
from Backend.database.db import SessionLocal
from Backend.database.models import Client

app = FastAPI(
    title="Advisor AI Backend",
    description="Enterprise AI Concierge Backend for Financial Advisors",
    version="1.0"
)

Base.metadata.create_all(bind=engine)

ingest_clients()

# Allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

system_metrics = {
    "ai_queries": 124,
    "compliance_alerts": 18,
    "uploaded_documents": 7,
    "active_sessions": 12,
    "market_events": 24
}

# Root route
@app.get("/")
def home():
    return {
        "message": "Advisor AI Backend Running Successfully"
    }

# Health check route
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

# Sample advisor endpoint
@app.get("/advisor/summary")
def advisor_summary():
    return {
        "advisor": "Demo Advisor",
        "clients": 42,
        "aum": "$12.5M",
        "risk_alerts": 3
    }

@app.post("/advisor/chat")
def advisor_chat(request: dict):

    user_query = request["query"]

    conversation_history = request.get("history", [])

    ai_response = generate_ai_response(
        user_query,
        conversation_history
    )

    return {
        "response": ai_response
    }

@app.post("/rag/query")
def rag_query(request: dict):

    question = request["question"]
    session_id = request.get("session_id", "default")

    print("\n[API] Question received:", question)

    answer = ask_rag(question, session_id)

    print("\n[API] Answer generated:", answer)

    return {
        "question": question,
        "answer": answer,
        "session_id": session_id
    }

@app.get("/memory/{session_id}")
def fetch_memory(session_id: str):

    history = get_history(session_id)

    return {
        "session_id": session_id,
        "history": history
    }

@app.post("/portfolio/analyze")
def portfolio_analyze(request: dict):

    equity = request["equity"]
    bonds = request["bonds"]
    cash = request["cash"]

    result = analyze_portfolio(
        equity,
        bonds,
        cash
    )

    return result

@app.post("/compliance/check")
def compliance_check(request: dict):

    client_profile = request["client_profile"]

    equity_allocation = request["equity_allocation"]

    result = check_compliance(
        client_profile,
        equity_allocation
    )

    return result

@app.post("/recommendations/generate")
def recommendation_api(request: dict):

    client_profile = request["client_profile"]

    equity = request["equity"]

    bonds = request["bonds"]

    cash = request["cash"]

    result = generate_recommendations(
        client_profile,
        equity,
        bonds,
        cash
    )

    return result

@app.post("/insights/generate")

def generate_insights(data: dict):

    insights = []

    equity = data["equity"]

    bonds = data["bonds"]

    cash = data["cash"]

    profile = data["client_profile"]

    # -----------------------------
    # HIGH EQUITY RISK
    # -----------------------------
    if equity >= 80:

        insights.append({

            "severity": "High",

            "type": "Aggressive Exposure",

            "message":
                "Portfolio has very high equity exposure and may experience elevated volatility."
        })

    # -----------------------------
    # LOW DIVERSIFICATION
    # -----------------------------
    if bonds < 15:

        insights.append({

            "severity": "Medium",

            "type": "Diversification Alert",

            "message":
                "Fixed income allocation may be insufficient for stability."
        })

    # -----------------------------
    # EXCESS CASH
    # -----------------------------
    if cash >= 25:

        insights.append({

            "severity": "Low",

            "type": "Cash Utilization",

            "message":
                "Large cash allocation detected. Consider reallocating idle capital."
        })

    # -----------------------------
    # CONSERVATIVE UNDEREXPOSURE
    # -----------------------------
    if profile == "conservative" and equity > 60:

        insights.append({

            "severity": "High",

            "type": "Suitability Risk",

            "message":
                "Equity allocation may not align with conservative investor objectives."
        })

    # -----------------------------
    # AGGRESSIVE UNDERALLOCATION
    # -----------------------------
    if profile == "aggressive" and equity < 60:

        insights.append({

            "severity": "Medium",

            "type": "Growth Opportunity",

            "message":
                "Aggressive investor profile may benefit from higher growth exposure."
        })

    # -----------------------------
    # HEALTHY BALANCE
    # -----------------------------
    if 50 <= equity <= 70 and bonds >= 20:

        insights.append({

            "severity": "Low",

            "type": "Portfolio Health",

            "message":
                "Portfolio allocation appears reasonably balanced."
        })

    return {
        "insights": insights
    }

@app.get("/clients")
def fetch_clients():

    return {
        "clients": get_all_clients()
    }

@app.get("/clients/{client_name}")
def fetch_client(client_name: str):

    client = get_client(client_name)

    return {
        "client": client
    }

# -----------------------------
# LOGIN API
# -----------------------------
@app.post("/login")
def login(data: dict):

    username = data.get("username")

    password = data.get("password")

    # -----------------------------
    # AUTHENTICATE
    # -----------------------------
    user = authenticate_user(
        username,
        password
    )

    if not user:

        return {
            "status": "error",
            "message": "Invalid credentials"
        }

    # -----------------------------
    # CREATE TOKEN
    # -----------------------------
    token = create_access_token({
        "sub": username,
        "role": user["role"]
    })

    return {
        "status": "success",
        "access_token": token,
        "role": user["role"]
    }

@app.get("/graph/{client_name}")
def graph_relationships(client_name: str):

    return get_client_relationships(client_name)

@app.post("/agent/query")
def multi_agent_query(data: dict):

    query = data["query"]

    result = route_query(query)

    return result

@app.get("/market/events")
def get_market_event():

    return generate_market_event()

@app.get("/market/intelligence")
def market_intelligence():

    event = generate_market_event()

    alerts = process_market_event(event)

    return {
        "market_event": event,
        "ai_alerts": alerts
    }

from fastapi import UploadFile, File
import os

@app.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...)):

    upload_path = f"temp_{file.filename}"

    with open(upload_path, "wb") as f:

        content = await file.read()

        f.write(content)

    result = ingest_pdf(upload_path)

    os.remove(upload_path)

    return result

@app.get("/system/metrics")
def get_system_metrics():

    return system_metrics

@app.get("/analytics/summary")

def analytics_summary():

    db = SessionLocal()

    clients = db.query(Client).all()

    total_clients = len(clients)

    total_aum = sum(
        int(client.aum)
        for client in clients
    )

    avg_return = round(

        sum(float(client.annual_return)
        for client in clients)

        / total_clients,

        2
    )

    risk_distribution = {

        "Conservative": len(
            [c for c in clients if c.risk == "Conservative"]
        ),

        "Moderate": len(
            [c for c in clients if c.risk == "Moderate"]
        ),

        "Aggressive": len(
            [c for c in clients if c.risk == "Aggressive"]
        )
    }

    db.close()

    return {

        "total_clients": total_clients,

        "total_aum": total_aum,

        "avg_return": avg_return,

        "risk_distribution": risk_distribution
    }