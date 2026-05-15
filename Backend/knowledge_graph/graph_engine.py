import networkx as nx

# -----------------------------
# CREATE KNOWLEDGE GRAPH
# -----------------------------
graph = nx.DiGraph()

# -----------------------------
# CLIENTS
# -----------------------------
clients = {
    "John Anderson": {
        "risk": "Conservative",
        "sector": "Technology"
    },
    "Sarah Williams": {
        "risk": "Moderate",
        "sector": "Healthcare"
    },
    "Michael Chen": {
        "risk": "Aggressive",
        "sector": "Technology"
    },
    "Priya Sharma": {
        "risk": "Moderate",
        "sector": "Finance"
    }
}

# -----------------------------
# BUILD GRAPH RELATIONSHIPS
# -----------------------------
for client, details in clients.items():

    graph.add_node(
        client,
        type="client"
    )

    graph.add_node(
        details["risk"],
        type="risk_profile"
    )

    graph.add_node(
        details["sector"],
        type="sector"
    )

    # Relationships
    graph.add_edge(
        client,
        details["risk"],
        relationship="has_risk"
    )

    graph.add_edge(
        client,
        details["sector"],
        relationship="invested_in"
    )

# -----------------------------
# GRAPH QUERY FUNCTION
# -----------------------------
def get_client_relationships(client_name):

    if client_name not in graph:

        return {
            "relationships": []
        }

    relationships = []

    for neighbor in graph.neighbors(client_name):

        relationship = graph[
            client_name
        ][neighbor]["relationship"]

        relationships.append({
            "target": neighbor,
            "relationship": relationship
        })

    return {
        "client": client_name,
        "relationships": relationships
    }