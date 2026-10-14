"""
Track 1: Action Agent Engine (Multi-Hop Reasoning & Automated Response)
Uses FalkorDB graph traversal as internal agent reasoning tools.
Selects tools dynamically, executes actions, and returns explainable decision paths.
"""

import time
import uuid
from typing import Any, Dict, List, Optional
from scout.db import FalkorGraph
from scout.brain import CompanyBrain
from scout.memory import AgentMemory

class ScoutActionAgent:
    def __init__(self, agent_id: str = "AGT-01", db: Optional[FalkorGraph] = None):
        self.agent_id = agent_id
        self.db = db or FalkorGraph.get_instance()
        self.brain = CompanyBrain(self.db)
        self.memory = AgentMemory(self.db)

    def investigate_incident(self, incident_id: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Multi-Hop Autonomous Investigation:
        Hop 1: Incident -> Triggering Log
        Hop 2: Incident -> Affected Asset
        Hop 3: Asset -> Employee Access History (Company Brain)
        Hop 4: Interaction -> Past Concept Solutions (Agent Memory)
        Hop 5: Autonomous Action & Tool Selection
        """
        hops_trace = []

        # Hop 1 & 2: Incident -> Log & Asset
        cypher_hop1 = """
        MATCH (inc:Incident {id: $id})
        OPTIONAL MATCH (inc)-[:TRIGGERED_BY]->(l:Log)
        OPTIONAL MATCH (inc)-[:AFFECTS]->(a:Asset)
        RETURN inc.id AS incident_id,
               inc.title AS title,
               inc.severity AS severity,
               inc.status AS status,
               collect(DISTINCT {id: l.id, message: l.message, level: l.level}) AS trigger_logs,
               a.id AS asset_id,
               a.name AS asset_name,
               a.tier AS asset_tier,
               a.ip AS asset_ip
        """
        res_hop1 = self.db.query_dicts(cypher_hop1, {"id": incident_id})
        if not res_hop1:
            return {"error": f"Incident {incident_id} not found in FalkorDB"}

        inc_info = res_hop1[0]
        hops_trace.append({
            "hop": 1,
            "description": "Correlated incident with telemetry trigger logs and target infrastructure.",
            "data": {
                "incident": inc_info["title"],
                "severity": inc_info["severity"],
                "logs_found": len(inc_info["trigger_logs"]),
                "target_asset": inc_info["asset_name"]
            }
        })

        asset_id = inc_info.get("asset_id")
        blast_radius = {}
        if asset_id:
            # Hop 3: Query Company Brain for Blast Radius
            blast_radius = self.brain.compute_blast_radius(asset_id)
            hops_trace.append({
                "hop": 2,
                "description": "Computed multi-hop organizational blast radius through Company Brain.",
                "data": {
                    "asset_tier": inc_info.get("asset_tier"),
                    "exposed_employees": blast_radius.get("exposed_employees", []),
                    "affected_projects": blast_radius.get("affected_projects", []),
                    "risk_score": blast_radius.get("calculated_risk_score")
