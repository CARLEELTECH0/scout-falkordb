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
