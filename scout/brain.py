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
               collect(DISTINCT a.name) AS accessed_assets
        """
        rows = self.db.query_dicts(cypher, {"id": employee_id})
        return rows[0] if rows else {}

    def compute_blast_radius(self, asset_id: str) -> Dict[str, Any]:
        """
        Compute the organizational and security blast radius if an asset is compromised.
        Finds:
        1. All employees with direct access.
        2. All projects relying on or associated with those employees.
        3. All sensitive documents linked to those projects.
        4. Any active incidents on the asset.
        """
        cypher = """
        MATCH (a:Asset {id: $id})
        OPTIONAL MATCH (inc:Incident)-[:AFFECTS]->(a)
        OPTIONAL MATCH (e:Employee)-[:ACCESSED]->(a)
        OPTIONAL MATCH (e)-[:ASSIGNED_TO]->(p:Project)
        OPTIONAL MATCH (p)-[:CONTAINS]->(d:Document)
        RETURN a.id AS asset_id,
               a.name AS asset_name,
               a.tier AS tier,
               a.type AS asset_type,
               collect(DISTINCT inc.id) AS related_incidents,
               collect(DISTINCT e.name) AS exposed_employees,
               collect(DISTINCT p.name) AS affected_projects,
               collect(DISTINCT d.title) AS exposed_documents
        """
        rows = self.db.query_dicts(cypher, {"id": asset_id})
        if not rows:
            return {"error": f"Asset {asset_id} not found"}
        res = rows[0]
        # Calculate risk score
        risk_score = (
            len(res.get("exposed_employees", [])) * 10 +
            len(res.get("affected_projects", [])) * 25 +
            len(res.get("exposed_documents", [])) * 20 +
            (50 if res.get("tier") == "Tier-0" else 20)
        )
        res["calculated_risk_score"] = risk_score
        res["severity"] = "CRITICAL" if risk_score > 100 else ("HIGH" if risk_score > 50 else "MEDIUM")
        return res

    def audit_access_path(self, employee_id: str, asset_id: str) -> List[Dict[str, Any]]:
        """Explain the relationship path between an employee and an asset."""
        cypher = """
        MATCH path = (e:Employee {id: $emp_id})-[*1..3]-(a:Asset {id: $asset_id})
        RETURN [n in nodes(path) | {id: n.id, label: labels(n)[0], name: coalesce(n.name, n.title)}] AS nodes,
               [r in relationships(path) | type(r)] AS relationships
        LIMIT 5
        """
        rows = self.db.query_dicts(cypher, {"emp_id": employee_id, "asset_id": asset_id})
        return rows

    def get_project_provenance(self, project_id: str) -> Dict[str, Any]:
        """Audit project team members, associated sensitive documents, and accessed assets."""
        cypher = """
        MATCH (p:Project {id: $id})
        OPTIONAL MATCH (e:Employee)-[:ASSIGNED_TO]->(p)
        OPTIONAL MATCH (p)-[:CONTAINS]->(d:Document)
        OPTIONAL MATCH (e)-[:ACCESSED]->(a:Asset)
        RETURN p.id AS project_id,
