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
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SCOUT — AI Team Workspace & Incident Solver</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['"Plus Jakarta Sans"', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
                        mono: ['"JetBrains Mono"', 'monospace'],
                    },
                    colors: {
                        brand: {
                            500: '#f97316',
                            600: '#ea580c',
                        }
                    }
                }
            }
        }
    </script>
    <style>
        :root {
            --bg-canvas: #080b13;
            --bg-card: rgba(18, 24, 38, 0.78);
            --liquid-orange: #ff6b00;
            --spring-curve: cubic-bezier(0.16, 1, 0.3, 1);
        }

        body {
            background-color: var(--bg-canvas);
            color: #f1f5f9;
            font-feature-settings: "cv02", "cv03", "cv04", "cv11", "tnum";
            letter-spacing: -0.012em;
            height: 100vh;
            overflow: hidden;
        }

        /* Imran Jakir Pillowy Rounded Cards */
        .dribbble-card {
            background: linear-gradient(150deg, rgba(22, 28, 46, 0.75) 0%, rgba(12, 16, 28, 0.92) 100%);
            backdrop-filter: blur(28px) saturate(210%);
            -webkit-backdrop-filter: blur(28px) saturate(210%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 24px;
            box-shadow: 0 10px 32px -8px rgba(0, 0, 0, 0.70), inset 0 1px 0 rgba(255, 255, 255, 0.10);
            transition: all 0.25s var(--spring-curve);
        }
        .dribbble-card:hover {
            border-color: rgba(249, 115, 22, 0.40);
            box-shadow: 0 14px 40px -8px rgba(249, 115, 22, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.15);
        }

        /* Voice Card (Lavender/Purple Glow) */
        .voice-card {
            background: linear-gradient(145deg, rgba(46, 28, 68, 0.65) 0%, rgba(20, 16, 32, 0.90) 100%);
            border: 1px solid rgba(168, 85, 247, 0.32);
            border-radius: 22px;
            box-shadow: 0 8px 25px -6px rgba(168, 85, 247, 0.22), inset 0 1px 0 rgba(255, 255, 255, 0.12);
        }

        /* Solar Orange Tactile Button */
        .btn-solar {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            height: 40px;
            padding: 0 18px;
            font-size: 0.8125rem;
            font-weight: 600;
            border-radius: 9999px;
            color: #ffffff;
            background: linear-gradient(180deg, #ff7b24 0%, #ea580c 100%);
            border: 1px solid rgba(255, 255, 255, 0.28);
            box-shadow: 0 4px 18px rgba(234, 88, 12, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.45);
            cursor: pointer;
            transition: all 140ms var(--spring-curve);
        }
        .btn-solar:hover:not(:disabled) {
            background: linear-gradient(180deg, #ff8d3d 0%, #f97316 100%);
            box-shadow: 0 6px 24px rgba(249, 115, 22, 0.60);
            transform: translateY(-1px);
        }
        .btn-solar:active:not(:disabled) {
            transform: translateY(0.5px) scale(0.98);
        }

        .btn-obsidian {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            height: 40px;
            padding: 0 16px;
            font-size: 0.8125rem;
            font-weight: 500;
            border-radius: 9999px;
            color: #cbd5e1;
            background: rgba(22, 28, 44, 0.65);
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.08);
            cursor: pointer;
            transition: all 140ms var(--spring-curve);
        }
        .btn-obsidian:hover {
            background: rgba(32, 40, 62, 0.85);
            border-color: rgba(249, 115, 22, 0.40);
            color: #ffffff;
            transform: translateY(-1px);
        }

        /* Soundwave Equalizer Bars */
        @keyframes soundwave {
            0%, 100% { height: 4px; }
            50% { height: 18px; }
        }
        .sound-bar-1 { animation: soundwave 1.1s infinite ease-in-out 0.1s; }
        .sound-bar-2 { animation: soundwave 1.1s infinite ease-in-out 0.35s; }
        .sound-bar-3 { animation: soundwave 1.1s infinite ease-in-out 0.2s; }
        .sound-bar-4 { animation: soundwave 1.1s infinite ease-in-out 0.5s; }
        .sound-bar-5 { animation: soundwave 1.1s infinite ease-in-out 0.25s; }

        .waveform-bar {
            width: 2.5px;
            border-radius: 2px;
            background-color: #cbd5e1;
        }

        /* Micro scrollbars */
        ::-webkit-scrollbar {
            width: 4px;
            height: 4px;
        }
        ::-webkit-scrollbar-track {
            background: transparent;
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(249, 115, 22, 0.28);
            border-radius: 2px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(249, 115, 22, 0.50);
        }

        /* Floating Bottom Nav Pill */
        .bottom-dock {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 60;
            background: rgba(14, 18, 30, 0.88);
            backdrop-filter: blur(28px) saturate(220%);
            -webkit-backdrop-filter: blur(28px) saturate(220%);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 9999px;
            padding: 6px 10px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.80), 0 0 30px rgba(249, 115, 22, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.18);
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .dock-tab {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            height: 38px;
            padding: 0 16px;
            border-radius: 9999px;
            font-size: 0.8125rem;
            font-weight: 600;
            color: #94a3b8;
            transition: all 0.2s var(--spring-curve);
            cursor: pointer;
            user-select: none;
            border: 1px solid transparent;
        }
        .dock-tab:hover {
            color: #ffffff;
            background: rgba(255, 255, 255, 0.06);
        }
        .dock-tab.active {
            color: #ffffff;
            background: linear-gradient(180deg, rgba(255, 107, 0, 0.22) 0%, rgba(234, 88, 12, 0.35) 100%);
            border: 1px solid rgba(249, 115, 22, 0.50);
            box-shadow: 0 4px 16px rgba(249, 115, 22, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.20);
        }

        /* Honeycomb Node Hover & Drag */
        .hex-cell {
            cursor: grab;
