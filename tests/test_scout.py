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


def test_honeycomb_color_encoding_and_quarantine():
    """
    Verify Track 1 & Track 3 UI business rules:
    - Employees are encoded as people (secondary color mapping).
    - Incidents and quarantined assets are mapped to primary RGY statuses.
    """
    db = FalkorGraph.get_instance()
    # Check employee nodes exist for secondary color assignment
    employees = db.query("MATCH (e:Employee) RETURN e.id, e.name")
    assert len(employees) == 10

    # Verify quarantine status updates in graph upon mitigation
    agent = ScoutActionAgent("AGT-01")
    agent.investigate_incident("INC-2026-001")
    quarantined = db.query("MATCH (a:Asset {status: 'Quarantined'}) RETURN a.name")
    assert len(quarantined) >= 1


def test_attack_simulator():
    """Verify AttackSimulator triggers scenario pulses, mutates FalkorDB, and triages."""
    from scout.simulator import AttackSimulator
    sim = AttackSimulator()
    scenarios = sim.list_scenarios()
    assert len(scenarios) >= 4

    res = sim.trigger_attack(vector="AUTH_BRUTE_FORCE")
    assert res["status"] == "Triggered"
    assert res["target_asset_id"] == "AST-01"
    assert "triage_result" in res
    assert res["triage_result"]["investigation"]["final_status"] == "Contained"


def test_evidence_exporter():
    """Verify EvidenceExporter generates cryptographically hashed post-mortem bundles."""
    from scout.exporter import EvidenceExporter
    exp = EvidenceExporter()
    bundle = exp.generate_incident_bundle("INC-2026-001")
    assert "incident_id" in bundle
    assert bundle["incident_id"] == "INC-2026-001"
    assert "integrity_checksum" in bundle
    assert len(bundle["integrity_checksum"]) == 64  # SHA-256 hex string

    md = exp.export_markdown("INC-2026-001")
    assert "Scout Incident Post-Mortem & Evidence Bundle" in md
    assert "INC-2026-001" in md
    assert "Organizational Blast Radius" in md


def test_tactical_audio_synthesizer():
    """Verify TacticalAudioSynthesizer generates phonetic scripts and tactical voice payloads."""
    from scout.audio import TacticalAudioSynthesizer
    synth = TacticalAudioSynthesizer()
    cues = synth.list_cues()
    assert "BREACH_ALERT" in cues
    assert "CONTAINMENT_SUCCESS" in cues
    assert "BLAST_RADIUS_WARNING" in cues
    assert "DIRECTIVE_ACK" in cues

    payload = synth.generate_cue("BREACH_ALERT", {"asset_name": "prod-auth-gateway"})
    assert payload["callsign"] == "Scout-Alpha"
    assert "prod-auth-gateway" in payload["spoken_text"]
    assert payload["soundwave_active"] is True
    assert 0.8 <= payload["pitch"] <= 1.2



