#!/usr/bin/env python3
"""
Scout CLI Runner & Demo Orchestrator
Usage:
  python run.py seed    -> Resets and seeds FalkorDB with unified enterprise schema
  python run.py serve   -> Launches FastAPI API and Interactive Live Graph Dashboard
  python run.py demo    -> Executes multi-hop autonomous security investigation demo
  python run.py mcp     -> Starts standard Model Context Protocol (MCP) server
"""

import sys
import uvicorn
from scout.seed import seed_enterprise_graph
from scout.brain import CompanyBrain
from scout.memory import AgentMemory
from scout.agent import ScoutActionAgent

def run_demo():
    print("=" * 70)
    print("   SCOUT: AUTONOMOUS ENTERPRISE KNOWLEDGE & SECURITY INVESTIGATOR")
    print("      Powered by FalkorDB (Graph Hacks Hackathon 2026)")
    print("=" * 70)

    seed_enterprise_graph()

    print("\n--- [TRACK 3: COMPANY BRAIN] ---")
    brain = CompanyBrain()
    asset_id = "AST-01"
    print(f"[*] Calculating Multi-Hop Blast Radius for {asset_id} (prod-auth-gateway)...")
    blast = brain.compute_blast_radius(asset_id)
    print(f"    - Risk Score: {blast.get('calculated_risk_score')} [{blast.get('severity')}]")
    print(f"    - Exposed Employees: {blast.get('exposed_employees')}")
    print(f"    - Downstream Projects: {blast.get('affected_projects')}")
    print(f"    - Sensitive Documents at Risk: {blast.get('exposed_documents')}")

    print("\n--- [TRACK 2: AGENT MEMORY & COORDINATION] ---")
    memory = AgentMemory()
    session_id = memory.start_session("AGT-01", "EMP-02", "Investigating Gateway Anomalies")
    print(f"[*] Initialized Graph Memory Session: {session_id}")
    procedural = memory.recall_procedural_memory("BruteForceSpike")
