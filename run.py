#!/usr/bin/env python3
"""
Scout CLI Runner & Demo Orchestrator
Usage:
  python run.py seed      -> Resets and seeds FalkorDB with unified enterprise schema
  python run.py serve     -> Launches FastAPI API and Interactive Live Graph Dashboard
  python run.py demo      -> Executes multi-hop autonomous security investigation demo
  python run.py simulate  -> Starts 24/7 background SOC threat generation daemon
  python run.py mcp       -> Starts standard Model Context Protocol (MCP) server
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
    print(f"[*] Recalled Past Procedural Memory for 'BruteForceSpike':")
    if procedural:
        print(f"    - Historical Tools Used: {procedural[0].get('tools_used')}")
        print(f"    - Past Resolution Pattern: {procedural[0].get('past_solutions')[:1]}")

    print("\n--- [TRACK 1: ACTION AGENT MULTI-HOP INVESTIGATION] ---")
    agent = ScoutActionAgent(agent_id="AGT-01")
    incident_id = "INC-2026-001"
    print(f"[*] Dispatching Scout Autonomous Investigator on {incident_id}...")
    result = agent.investigate_incident(incident_id, session_id=session_id)

    print("\n[+] MULTI-HOP REASONING TRACE:")
    for hop in result.get("reasoning_hops", []):
        print(f"    Hop {hop['hop']}: {hop['description']}")
        print(f"      -> Data: {hop['data']}")

    print("\n[+] EXPLAINABLE VERDICT & RESOLUTION:")
    print(f"    {result.get('explainable_verdict')}")
    print(f"    Final Status: {result.get('final_status')}")
    print(f"    Mitigation Tool Executed: {result.get('tools_used')}")

    print("\n--- [TRACK 2: MULTI-AGENT HANDOFF] ---")
    handoff = memory.handoff_agent_task(
        from_agent_id="AGT-01",
        to_agent_id="AGT-02",
        reason="Quarantine verified; transfer to Remediator for IAM credential rotation",
        incident_id=incident_id
    )
    print(f"[+] Multi-Agent Task Transferred in Graph: {handoff['from_agent']} -> {handoff['to_agent']}")
    print("=" * 70)
    print("All 3 tracks demonstrated with 100% Cypher-driven graph execution!")

def main():
    if len(sys.argv) < 2 or sys.argv[1] == "demo":
        run_demo()
    elif sys.argv[1] == "seed":
        seed_enterprise_graph()
    elif sys.argv[1] == "serve":
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000
        print(f"[*] Launching Scout Dashboard at http://localhost:{port}")
        uvicorn.run("scout.api:app", host="0.0.0.0", port=port, reload=True)
    elif sys.argv[1] == "simulate":
        from scout.simulator import AttackSimulator
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 15
        count = int(sys.argv[3]) if len(sys.argv) > 3 else None
        sim = AttackSimulator()
        sim.run_daemon(interval_seconds=interval, max_iterations=count)
    elif sys.argv[1] == "mcp":
        from scout.mcp_server import main as mcp_main
        mcp_main()
    else:
        print(f"Unknown command: {sys.argv[1]}")
        print("Available: demo, seed, serve, simulate, mcp")

if __name__ == "__main__":
    main()
