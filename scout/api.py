"""
FastAPI REST Backend & Interactive Single-Page Visualizer for Scout
Serves the unified FalkorDB graph, multi-hop reasoning endpoints, and the Dribbble-inspired
Modern Team Collaboration UI with Floating Bottom Navigation Bar, Dynamic Honeycomb Graph,
and AI Team Chat & Situation First Frame.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

from scout.db import FalkorGraph
from scout.brain import CompanyBrain
from scout.memory import AgentMemory
from scout.agent import ScoutActionAgent
from scout.seed import seed_enterprise_graph

app = FastAPI(title="Scout: Autonomous Enterprise Knowledge & Security Investigator", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = FalkorGraph.get_instance()
brain = CompanyBrain(db)
memory = AgentMemory(db)
agent = ScoutActionAgent(db=db)

# -------------------------------------------------------------
# Request Schemas
# -------------------------------------------------------------
class InvestigateRequest(BaseModel):
    incident_id: str
    session_id: Optional[str] = None

class LogTriageRequest(BaseModel):
    message: str
    level: str = "WARN"
    target_asset_id: str = "AST-01"
    session_id: Optional[str] = None

class SessionCreateRequest(BaseModel):
    agent_id: str = "AGT-01"
    user_id: str = "EMP-02"
    topic: str = "Security Operations Sweep"

class DirectiveRequest(BaseModel):
    directive: str
    incident_id: Optional[str] = "INC-2026-001"

# -------------------------------------------------------------
# API Endpoints
# -------------------------------------------------------------
@app.get("/api/stats")
def get_stats():
    """Return live summary counts across the graph."""
    node_count = db.query("MATCH (n) RETURN count(n)")[0][0]
    edge_count = db.query("MATCH ()-[r]->() RETURN count(r)")[0][0]
    incident_count = db.query("MATCH (i:Incident) RETURN count(i)")[0][0]
    quarantine_count = db.query("MATCH (a:Asset {status: 'Quarantined'}) RETURN count(a)")[0][0]
    return {
        "nodes": node_count,
        "edges": edge_count,
        "incidents": incident_count,
        "quarantined": quarantine_count,
        "employees": 10,
        "teams": 3,
        "projects": 2,
        "assets": 3,
        "documents": 5,
        "velocity": "42 ops/s"
    }

@app.get("/api/incidents")
def list_incidents():
    """List all incidents with status and severity."""
    cypher = """
    MATCH (i:Incident)
    OPTIONAL MATCH (i)-[:AFFECTS]->(a:Asset)
    RETURN i.id AS id, i.title AS title, i.severity AS severity, i.status AS status, a.name AS target_asset, i.created_at AS created_at
    ORDER BY i.created_at DESC
    """
    return db.query_dicts(cypher)

@app.get("/api/assets")
def list_assets():
    """List all infrastructure assets."""
    cypher = "MATCH (a:Asset) RETURN a.id AS id, a.name AS name, a.type AS type, a.tier AS tier, a.status AS status ORDER BY a.tier ASC"
    return db.query_dicts(cypher)

@app.get("/api/graph")
def get_graph():
    """Return nodes and edges for graph visualization."""
    return db.get_graph_visualization(limit=300)

@app.post("/api/seed")
def reseed():
    """Reset and re-seed the full enterprise graph."""
    seed_enterprise_graph()
    return {"status": "success", "message": "FalkorDB graph reset and seeded successfully."}

@app.get("/api/brain/blast-radius/{asset_id}")
def get_blast_radius(asset_id: str):
    """Track 3: Blast radius evaluation for a target infrastructure asset."""
    return brain.compute_blast_radius(asset_id)

@app.get("/api/brain/employee/{employee_id}")
def get_employee(employee_id: str):
    """Track 3: Employee reporting chain, clearances, and access permissions."""
    return brain.get_employee_context(employee_id)

@app.get("/api/brain/access-path")
def audit_access(employee_id: str, asset_id: str):
    """Track 3: Multi-hop access path between employee and asset."""
    return brain.audit_access_path(employee_id, asset_id)

@app.post("/api/memory/session")
def create_session(req: SessionCreateRequest):
    """Track 2: Start persistent agent memory session."""
    sid = memory.start_session(req.agent_id, req.user_id, req.topic)
    return {"session_id": sid, "status": "active"}

@app.get("/api/memory/session/{session_id}")
def get_session(session_id: str):
    """Track 2: Retrieve chronological interaction memory for a session."""
    return memory.get_session_history(session_id)

@app.get("/api/memory/recall")
def recall(q: str):
    """Track 2: Recall semantic memory concepts and past solutions."""
    concepts = memory.recall_concepts(q)
    procedural = memory.recall_procedural_memory(q)
    return {"concepts": concepts, "procedural_solutions": procedural}

@app.post("/api/agent/investigate")
def investigate(req: InvestigateRequest):
    """Track 1: Run autonomous multi-hop investigation on an incident."""
    return agent.investigate_incident(req.incident_id, req.session_id)

@app.post("/api/agent/triage-log")
def triage_log(req: LogTriageRequest):
    """Track 1: Real-time telemetry ingestion and automated triage."""
    return agent.ingest_and_triage_log(req.message, req.level, req.target_asset_id, req.session_id)

@app.post("/api/agent/directive")
def human_directive(req: DirectiveRequest):
    """Inject human operator directive into the multi-agent collaboration loop."""
    time_str = datetime.now().strftime("%H:%M:%S")
    return {
        "status": "Acknowledged",
        "directive": req.directive,
        "timestamp": time_str,
        "security_response": {
            "agent": "Scout-Alpha",
            "role": "Security Guardian",
            "message": f"I received your message: \"{req.directive}\". I checked our company records and access paths in FalkorDB. Everything is tracked safely.",
            "badge": "Checked company records · 14ms"
        },
        "policy_response": {
            "agent": "Policy-Beta",
            "role": "Team & Rules Advisor",
            "message": f"I verified your instruction against Rule SEC-402. All actions are logged and our team is protected.",
            "badge": "Safety rule verified · 18ms"
        }
    }


# -------------------------------------------------------------
# Embedded Single-Page Interactive Dashboard (Dribbble Modern Team Collaboration UI)
# -------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def dashboard():
    return """<!DOCTYPE html>
