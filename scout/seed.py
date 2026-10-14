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
