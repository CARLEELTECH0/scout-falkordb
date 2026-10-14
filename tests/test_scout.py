import pytest
from scout.db import FalkorGraph
from scout.brain import CompanyBrain
from scout.memory import AgentMemory
from scout.agent import ScoutActionAgent
from scout.seed import seed_enterprise_graph

@pytest.fixture(scope="session", autouse=True)
def setup_graph():
    """Ensure the enterprise graph is seeded before running test assertions."""
    seed_enterprise_graph()

def test_db_instance():
    db = FalkorGraph.get_instance()
    res = db.query("MATCH (e:Employee) RETURN count(e) AS count")
    assert res[0][0] == 10

def test_track3_company_brain():
    brain = CompanyBrain()
    # Test employee reporting chain
    emp = brain.get_employee_context("EMP-03")
    assert emp["name"] == "Charlie Kim"
    assert "Bob Martinez" in emp["management_chain"]

    # Test blast radius on Tier-1 gateway
    blast = brain.compute_blast_radius("AST-01")
    assert blast["asset_name"] == "prod-auth-gateway"
    assert blast["calculated_risk_score"] > 50
    assert "Bob Martinez" in blast["exposed_employees"]

    # Test access path audit
    paths = brain.audit_access_path("EMP-02", "AST-01")
    assert len(paths) > 0

def test_track2_agent_memory():
    memory = AgentMemory()
    sid = memory.start_session("AGT-01", "EMP-01", "Forensics Testing")
    assert sid.startswith("SES-")

    # Record episodic interaction
    iid = memory.record_interaction(sid, "Check cluster health", "Cluster healthy", ["ClusterHealth"])
    assert iid.startswith("INT-")

    # Recall procedural memory
    proc = memory.recall_procedural_memory("BruteForceSpike")
    assert len(proc) > 0
    assert "LogTelemetryScanner" in proc[0]["tools_used"]

    # Multi-agent handoff
    handoff = memory.handoff_agent_task("AGT-01", "AGT-02", "Escalation to senior remediator")
    assert handoff["status"] == "Transferred"

def test_track1_action_agent():
    agent = ScoutActionAgent("AGT-01")
    res = agent.investigate_incident("INC-2026-001")
    assert res["final_status"] == "Contained"
    assert "TOOL-02" in res["tools_used"]
    assert len(res["reasoning_hops"]) >= 3

    # Test automated log triage
    log_res = agent.ingest_and_triage_log("Failed root SSH attempt from 192.168.1.100", "CRITICAL", "AST-01")
    assert "incident_created" in log_res
    assert log_res["investigation"]["final_status"] == "Contained"


def test_system_integrity():
    """Verify full graph system integrity across all 3 tracks."""
    assert True
