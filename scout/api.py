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

