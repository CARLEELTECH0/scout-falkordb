from scout.db import FalkorGraph

def seed_enterprise_graph():
    db = FalkorGraph.get_instance()
    print("[*] Resetting and seeding unified Scout Enterprise Graph...")
    
    try:
        db.graph.delete()
        db.graph = db.client.select_graph(db.graph.name)
        db._init_indices()
    except Exception as e:
        print(f"[!] Warning resetting graph: {e}")

    # =========================================================================
    # Track 3: Company Brain (10 Employees, 3 Teams, 2 Projects, 5 Docs, 3 Assets)
    # =========================================================================
    employees = [
        {"id": "EMP-01", "name": "Alice Chen", "role": "CISO", "email": "alice@corp.internal", "clearance": "TopSecret"},
        {"id": "EMP-02", "name": "Bob Martinez", "role": "SecOps Lead", "email": "bob@corp.internal", "clearance": "Secret"},
        {"id": "EMP-03", "name": "Charlie Kim", "role": "Security Analyst", "email": "charlie@corp.internal", "clearance": "Confidential"},
        {"id": "EMP-04", "name": "Diana Prince", "role": "DevOps Lead", "email": "diana@corp.internal", "clearance": "Secret"},
        {"id": "EMP-05", "name": "Evan Wright", "role": "SRE Engineer", "email": "evan@corp.internal", "clearance": "Confidential"},
        {"id": "EMP-06", "name": "Fiona Gallagher", "role": "Data Architect", "email": "fiona@corp.internal", "clearance": "Secret"},
        {"id": "EMP-07", "name": "George Clark", "role": "Backend Engineer", "email": "george@corp.internal", "clearance": "Internal"},
        {"id": "EMP-08", "name": "Hannah Abbott", "role": "Frontend Engineer", "email": "hannah@corp.internal", "clearance": "Internal"},
        {"id": "EMP-09", "name": "Ian Malcolm", "role": "Product Manager", "email": "ian@corp.internal", "clearance": "Internal"},
        {"id": "EMP-10", "name": "Julia Roberts", "role": "Compliance Officer", "email": "julia@corp.internal", "clearance": "Secret"},
    ]
    for emp in employees:
        db.create_node("Employee", emp)

    reports = [
        ("EMP-02", "EMP-01"),
        ("EMP-03", "EMP-02"),
        ("EMP-04", "EMP-01"),
        ("EMP-05", "EMP-04"),
        ("EMP-07", "EMP-04"),
        ("EMP-08", "EMP-04"),
        ("EMP-06", "EMP-01"),
        ("EMP-09", "EMP-01"),
        ("EMP-10", "EMP-01"),
    ]
    for sub, sup in reports:
        db.create_edge("Employee", sub, "REPORTS_TO", "Employee", sup)

    teams = [
        {"id": "TEAM-01", "name": "SecOps", "department": "Information Security"},
        {"id": "TEAM-02", "name": "Cloud Platform", "department": "Infrastructure"},
        {"id": "TEAM-03", "name": "Core Product", "department": "Engineering"},
    ]
    for t in teams:
        db.create_node("Team", t)

    memberships = [
        ("EMP-01", "TEAM-01"), ("EMP-02", "TEAM-01"), ("EMP-03", "TEAM-01"),
        ("EMP-04", "TEAM-02"), ("EMP-05", "TEAM-02"),
        ("EMP-06", "TEAM-03"), ("EMP-07", "TEAM-03"), ("EMP-08", "TEAM-03"),
        ("EMP-09", "TEAM-03"), ("EMP-10", "TEAM-01"),
    ]
    for emp_id, team_id in memberships:
        db.create_edge("Employee", emp_id, "MEMBER_OF", "Team", team_id)

    projects = [
        {"id": "PRJ-01", "name": "Project FalconShield", "status": "Active", "risk": "Critical", "description": "Zero-trust IAM overhaul"},
        {"id": "PRJ-02", "name": "Project Horizon Cloud", "status": "Active", "risk": "Medium", "description": "Multi-region microservices deployment"},
    ]
    for p in projects:
        db.create_node("Project", p)

    assignments = [
        ("EMP-02", "PRJ-01"), ("EMP-03", "PRJ-01"), ("EMP-04", "PRJ-01"),
        ("EMP-05", "PRJ-02"), ("EMP-06", "PRJ-02"), ("EMP-07", "PRJ-02"),
    ]
    for emp_id, prj_id in assignments:
        db.create_edge("Employee", emp_id, "ASSIGNED_TO", "Project", prj_id)

    assets = [
        {"id": "AST-01", "name": "prod-auth-gateway", "type": "Server", "ip": "10.0.1.12", "tier": "Tier-1", "status": "Active"},
        {"id": "AST-02", "name": "prod-falcon-cluster", "type": "Database", "ip": "10.0.1.5", "tier": "Tier-0", "status": "Active"},
        {"id": "AST-03", "name": "k8s-worker-node-01", "type": "Server", "ip": "10.0.2.40", "tier": "Tier-2", "status": "Active"},
    ]
    for a in assets:
        db.create_node("Asset", a)

    access_edges = [
        ("EMP-02", "AST-01", {"protocol": "SSH", "last_active": "2026-10-14T08:12:00Z"}),
        ("EMP-04", "AST-01", {"protocol": "Bastion", "last_active": "2026-10-13T14:20:00Z"}),
        ("EMP-06", "AST-02", {"protocol": "PG-Wire", "last_active": "2026-10-14T09:00:00Z"}),
        ("EMP-07", "AST-02", {"protocol": "TLS", "last_active": "2026-10-14T09:15:00Z"}),
        ("EMP-05", "AST-03", {"protocol": "Kubectl", "last_active": "2026-10-14T07:45:00Z"}),
    ]
    for emp_id, ast_id, props in access_edges:
        db.create_edge("Employee", emp_id, "ACCESSED", "Asset", ast_id, props)

    docs = [
        {"id": "DOC-01", "title": "Zero-Trust Architecture Spec", "classification": "Secret", "uri": "s3://corp-docs/sec-01.pdf"},
        {"id": "DOC-02", "title": "FalkorDB Graph Cluster Runbook", "classification": "Confidential", "uri": "s3://corp-docs/db-02.md"},
        {"id": "DOC-03", "title": "IAM Incident Response Playbook", "classification": "Secret", "uri": "s3://corp-docs/playbook-03.pdf"},
        {"id": "DOC-04", "title": "Kubernetes Ingress Firewall Rules", "classification": "Confidential", "uri": "s3://corp-docs/k8s-04.yaml"},
        {"id": "DOC-05", "title": "Customer Data Retention Policy", "classification": "Internal", "uri": "s3://corp-docs/audit-05.pdf"},
    ]
    for d in docs:
        db.create_node("Document", d)

    project_docs = [
        ("PRJ-01", "DOC-01"), ("PRJ-01", "DOC-03"),
        ("PRJ-02", "DOC-02"), ("PRJ-02", "DOC-04"), ("PRJ-01", "DOC-05"),
    ]
    for prj_id, doc_id in project_docs:
        db.create_edge("Project", prj_id, "CONTAINS", "Document", doc_id)

    # =========================================================================
    # Track 2: Agent Memory & Coordination
    # =========================================================================
    agents = [
        {"id": "AGT-01", "name": "Scout-Investigator", "version": "1.0", "status": "Active", "specialty": "Triage"},
        {"id": "AGT-02", "name": "Scout-Remediator", "version": "1.0", "status": "Standby", "specialty": "Action"},
    ]
    for ag in agents:
        db.create_node("Agent", ag)

    sessions = [
        {"id": "SES-101", "user_id": "EMP-02", "created_at": "2026-10-14T08:00:00Z", "topic": "SSH Security Sweep"},
        {"id": "SES-102", "user_id": "EMP-04", "created_at": "2026-10-14T09:30:00Z", "topic": "Database Access Audit"},
    ]
    for s in sessions:
        db.create_node("Session", s)

    db.create_edge("Agent", "AGT-01", "HAS_SESSION", "Session", "SES-101")
    db.create_edge("Agent", "AGT-01", "HAS_SESSION", "Session", "SES-102")

    interactions = [
        {
            "id": "INT-01",
            "prompt": "Investigate anomalous SSH traffic from subnet 10.0.1.0/24",
            "response": "Identified high-velocity failed logins targeting prod-auth-gateway. Flagged INC-2026-001.",
            "timestamp": "2026-10-14T08:05:00Z"
        },
        {
            "id": "INT-02",
            "prompt": "Correlate access logs on prod-falcon-cluster with off-hours queries",
            "response": "Found bulk SELECT on customer_audit by EMP-07 outside shift hours. Flagged INC-2026-002.",
            "timestamp": "2026-10-14T09:35:00Z"
        }
    ]
    for inter in interactions:
        db.create_node("Interaction", inter)

    db.create_edge("Interaction", "INT-01", "RECORDED_IN", "Session", "SES-101")
    db.create_edge("Interaction", "INT-02", "RECORDED_IN", "Session", "SES-102")

    concepts = [
        {"id": "CPT-01", "name": "BruteForceSpike", "description": "Rapid succession of authentication failures indicating credential stuffing."},
        {"id": "CPT-02", "name": "PrivilegeEscalation", "description": "Elevation of access permissions across tier boundaries without ticket authorization."},
        {"id": "CPT-03", "name": "DataExfiltrationRisk", "description": "High-volume read query executed on Tier-0 database outside business hours."},
    ]
    for c in concepts:
        db.create_node("Concept", c)

    db.create_edge("Interaction", "INT-01", "RECALLS", "Concept", "CPT-01")
    db.create_edge("Interaction", "INT-02", "RECALLS", "Concept", "CPT-03")

    # =========================================================================
    # Track 1: Action Agent (Incidents, Tools, Logs, Handoffs)
    # =========================================================================
    tools = [
        {"id": "TOOL-01", "name": "LogTelemetryScanner", "category": "Telemetry", "permission": "ReadAudit"},
        {"id": "TOOL-02", "name": "FirewallQuarantine", "category": "Mitigation", "permission": "WriteNetwork"},
        {"id": "TOOL-03", "name": "GraphBlastRadiusAnalyzer", "category": "Forensics", "permission": "ReadGraph"},
        {"id": "TOOL-04", "name": "TokenRevocationEngine", "category": "Remediation", "permission": "WriteIAM"},
    ]
    for t in tools:
        db.create_node("Tool", t)

    logs = [
        {"id": "LOG-881", "level": "WARN", "message": "Failed SSH password for root from 10.0.1.45 port 42812", "timestamp": "2026-10-14T08:02:11Z"},
        {"id": "LOG-882", "level": "WARN", "message": "Failed SSH password for admin from 10.0.1.45 port 42814", "timestamp": "2026-10-14T08:02:15Z"},
        {"id": "LOG-903", "level": "INFO", "message": "Bulk query SELECT * FROM users_pii executed (50,000 rows returned)", "timestamp": "2026-10-14T09:32:00Z"},
    ]
    for l in logs:
        db.create_node("Log", l)

    incidents = [
        {"id": "INC-2026-001", "title": "Gateway Brute-Force Attack", "severity": "High", "status": "UnderInvestigation", "created_at": "2026-10-14T08:03:00Z"},
        {"id": "INC-2026-002", "title": "Anomalous Database Bulk Extraction", "severity": "Critical", "status": "Contained", "created_at": "2026-10-14T09:33:00Z"},
    ]
    for inc in incidents:
        db.create_node("Incident", inc)

    # Connections
    db.create_edge("Incident", "INC-2026-001", "TRIGGERED_BY", "Log", "LOG-881")
    db.create_edge("Incident", "INC-2026-001", "TRIGGERED_BY", "Log", "LOG-882")
    db.create_edge("Incident", "INC-2026-001", "AFFECTS", "Asset", "AST-01")

    db.create_edge("Incident", "INC-2026-002", "TRIGGERED_BY", "Log", "LOG-903")
    db.create_edge("Incident", "INC-2026-002", "AFFECTS", "Asset", "AST-02")

    # Agent Actions & Multi-Agent Handoff
    db.create_edge("Agent", "AGT-01", "INVESTIGATED", "Incident", "INC-2026-001")
    db.create_edge("Agent", "AGT-01", "USED_TOOL", "Tool", "TOOL-01")
    db.create_edge("Agent", "AGT-01", "USED_TOOL", "Tool", "TOOL-03")

    # Multi-Agent Coordination Handoff: Investigator -> Remediator
    db.create_edge("Agent", "AGT-01", "HANDED_OFF_TO", "Agent", "AGT-02", {"reason": "Mitigation Required", "incident": "INC-2026-002"})
    db.create_edge("Agent", "AGT-02", "USED_TOOL", "Tool", "TOOL-02")
    db.create_edge("Agent", "AGT-02", "USED_TOOL", "Tool", "TOOL-04")

    print("[+] Unified Scout Enterprise Graph successfully seeded!")
