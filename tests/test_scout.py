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
