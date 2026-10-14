"""
Track 3: Company Brain Engine
Connects employees, teams, projects, assets, and documents.
Provides multi-hop blast radius analysis and access path audits.
"""

from typing import Any, Dict, List, Optional
from scout.db import FalkorGraph

class CompanyBrain:
    def __init__(self, db: Optional[FalkorGraph] = None):
        self.db = db or FalkorGraph.get_instance()

    def get_employee_context(self, employee_id: str) -> Dict[str, Any]:
        """Fetch an employee's reporting chain, team, assigned projects, and accessed assets."""
        cypher = """
        MATCH (e:Employee {id: $id})
        OPTIONAL MATCH (e)-[:MEMBER_OF]->(t:Team)
        OPTIONAL MATCH (e)-[:REPORTS_TO*1..3]->(mgr:Employee)
        OPTIONAL MATCH (e)-[:ASSIGNED_TO]->(p:Project)
        OPTIONAL MATCH (e)-[:ACCESSED]->(a:Asset)
        RETURN e.id AS id, e.name AS name, e.role AS role, e.clearance AS clearance,
               t.name AS team,
               collect(DISTINCT mgr.name) AS management_chain,
               collect(DISTINCT p.name) AS projects,
