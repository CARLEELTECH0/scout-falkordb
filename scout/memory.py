"""
Track 2: Agent Memory & Coordination Engine
Maintains episodic, semantic, and procedural graph memory across sessions.
Enables high-concurrency memory queries and multi-agent handoffs.
"""

import time
import uuid
from typing import Any, Dict, List, Optional
from scout.db import FalkorGraph

class AgentMemory:
    def __init__(self, db: Optional[FalkorGraph] = None):
        self.db = db or FalkorGraph.get_instance()

    def start_session(self, agent_id: str, user_id: str, topic: str = "General Investigation") -> str:
        """Create a new agent session and bind to the agent."""
        session_id = f"SES-{uuid.uuid4().hex[:6].upper()}"
        props = {
            "id": session_id,
            "user_id": user_id,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "topic": topic
        }
        self.db.create_node("Session", props)
        self.db.create_edge("Agent", agent_id, "HAS_SESSION", "Session", session_id)
        return session_id

    def record_interaction(
        self,
        session_id: str,
        prompt: str,
        response: str,
        concept_names: Optional[List[str]] = None
    ) -> str:
        """Store an interaction (episodic memory) and link to semantic concepts."""
        interaction_id = f"INT-{uuid.uuid4().hex[:6].upper()}"
        props = {
            "id": interaction_id,
            "prompt": prompt,
            "response": response,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        self.db.create_node("Interaction", props)
        self.db.create_edge("Interaction", interaction_id, "RECORDED_IN", "Session", session_id)

        if concept_names:
            for c_name in concept_names:
                # Ensure concept exists
                c_id = f"CPT-{c_name.upper().replace(' ', '_')}"
                self.db.create_node("Concept", {"id": c_id, "name": c_name})
                self.db.create_edge("Interaction", interaction_id, "RECALLS", "Concept", c_id)

        return interaction_id

    def recall_concepts(self, keyword: str) -> List[Dict[str, Any]]:
        """Semantic Memory: Search for concepts and find all past interactions that recalled them."""
        cypher = """
        MATCH (c:Concept)
        WHERE toLower(c.name) CONTAINS toLower($kw) OR toLower(coalesce(c.description, '')) CONTAINS toLower($kw)
        OPTIONAL MATCH (i:Interaction)-[:RECALLS]->(c)
        RETURN c.id AS concept_id,
               c.name AS concept_name,
               c.description AS description,
               collect(DISTINCT {prompt: i.prompt, response: i.response, timestamp: i.timestamp}) AS past_interactions
        """
        return self.db.query_dicts(cypher, {"kw": keyword})

    def recall_procedural_memory(self, concept_name: str) -> List[Dict[str, Any]]:
        """Procedural Memory: What tools and steps did agents use when dealing with this concept?"""
        cypher = """
        MATCH (c:Concept)
        WHERE toLower(c.name) = toLower($name)
        MATCH (i:Interaction)-[:RECALLS]->(c)
        MATCH (i)-[:RECORDED_IN]->(s:Session)<-[:HAS_SESSION]-(a:Agent)
        OPTIONAL MATCH (a)-[:USED_TOOL]->(t:Tool)
        RETURN a.name AS agent_name,
               c.name AS concept,
               collect(DISTINCT t.name) AS tools_used,
               collect(DISTINCT i.response) AS past_solutions
        """
        return self.db.query_dicts(cypher, {"name": concept_name})

    def handoff_agent_task(
        self,
