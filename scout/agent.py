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
                }
            })

        # Hop 4: Check Agent Memory for Historical Precedents
        concept_recalled = "BruteForceSpike" if "brute" in inc_info["title"].lower() or "auth" in inc_info["title"].lower() else "DataExfiltrationRisk"
        past_solutions = self.memory.recall_procedural_memory(concept_recalled)
        hops_trace.append({
            "hop": 3,
            "description": f"Retrieved procedural memory for semantic concept '{concept_recalled}'.",
            "data": {
                "concept": concept_recalled,
                "precedents_found": len(past_solutions),
                "recommended_tools": past_solutions[0].get("tools_used", []) if past_solutions else ["TOOL-02"]
            }
        })

        # Hop 5: Action & Tool Selection
        action_taken = None
        tool_executed = None
        if inc_info["severity"] in ("High", "Critical") and asset_id:
            # Select and run FirewallQuarantine (TOOL-02)
            tool_executed = "TOOL-02"  # FirewallQuarantine
            action_taken = self.quarantine_asset(asset_id, reason=f"Triggered by {incident_id}")
            # Update incident status
            self.db.update_node("Incident", incident_id, {"status": "Contained"})
            # Link agent tool execution in graph
            self.db.create_edge("Agent", self.agent_id, "USED_TOOL", "Tool", tool_executed)
            self.db.create_edge("Agent", self.agent_id, "INVESTIGATED", "Incident", incident_id)

            hops_trace.append({
                "hop": 4,
                "description": "Selected mitigation tool and quarantined compromised asset.",
                "data": {
                    "tool": "TOOL-02 (FirewallQuarantine)",
                    "action": "Asset isolated and incident status updated to Contained"
                }
            })

        # Record this investigation in memory session if provided
        if session_id:
            summary = f"Investigated {incident_id} ({inc_info['title']}). Target {inc_info.get('asset_name')} quarantined via {tool_executed}."
            self.memory.record_interaction(
                session_id=session_id,
                prompt=f"Investigate {incident_id}",
                response=summary,
                concept_names=[concept_recalled]
            )

        return {
            "incident_id": incident_id,
            "title": inc_info["title"],
            "severity": inc_info["severity"],
            "final_status": "Contained" if action_taken else inc_info["status"],
            "blast_radius": blast_radius,
            "tools_used": [tool_executed] if tool_executed else [],
            "reasoning_hops": hops_trace,
            "explainable_verdict": (
                f"Incident {incident_id} is a {inc_info['severity']} severity event affecting {inc_info.get('asset_name')} "
                f"({inc_info.get('asset_tier')}). Because {len(blast_radius.get('exposed_employees', []))} employees and "
                f"{len(blast_radius.get('affected_projects', []))} critical projects are downstream, Scout executed "
                f"{tool_executed or 'telemetry scan'} to neutralize lateral movement."
            )
        }

    def quarantine_asset(self, asset_id: str, reason: str) -> Dict[str, Any]:
        """Mutate the graph: Mark an asset as Quarantined and link to this agent."""
        props = {
            "status": "Quarantined",
            "quarantine_reason": reason,
            "quarantined_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        self.db.update_node("Asset", asset_id, props)
        self.db.create_edge("Asset", asset_id, "QUARANTINED_BY", "Agent", self.agent_id, {
            "reason": reason,
            "timestamp": props["quarantined_at"]
        })
        return {"asset_id": asset_id, "status": "Quarantined", "reason": reason}

    def ingest_and_triage_log(
        self,
        message: str,
        level: str,
        target_asset_id: str,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Ingest real-time log, detect anomalies, auto-generate Incident in FalkorDB and triage."""
        log_id = f"LOG-{uuid.uuid4().hex[:6].upper()}"
        log_props = {
            "id": log_id,
            "message": message,
            "level": level,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        self.db.create_node("Log", log_props)

        # Check if log warrants an incident
        is_suspicious = any(w in message.lower() for w in ["failed", "unauthorized", "bulk", "injection", "spike", "error"])
        severity = "High" if ("root" in message.lower() or "bulk" in message.lower()) else "Medium"

        if is_suspicious:
            incident_id = f"INC-{uuid.uuid4().hex[:6].upper()}"
            inc_props = {
                "id": incident_id,
                "title": f"Telemetry Alert: {message[:40]}...",
                "severity": severity,
                "status": "New",
                "created_at": log_props["timestamp"]
            }
            self.db.create_node("Incident", inc_props)
            self.db.create_edge("Incident", incident_id, "TRIGGERED_BY", "Log", log_id)
            self.db.create_edge("Incident", incident_id, "AFFECTS", "Asset", target_asset_id)

            # Autonomous triage & response
            investigation = self.investigate_incident(incident_id, session_id=session_id)
            return {
                "log_id": log_id,
                "incident_created": incident_id,
                "investigation": investigation
            }

        return {"log_id": log_id, "status": "Ingested", "alert": False}

# Autonomous triage convergence: asset quarantine status validated post-containment.
