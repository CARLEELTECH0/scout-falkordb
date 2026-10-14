import os
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from scout import config

class FalkorGraph:
    _instance = None

    def __init__(self):
        if config.USE_EMBEDDED:
            from redislite import FalkorDB as EmbeddedFalkorDB
            db_dir = Path(config.DB_PATH).parent
            db_dir.mkdir(parents=True, exist_ok=True)
            self.client = EmbeddedFalkorDB(config.DB_PATH)
        else:
            from falkordb import FalkorDB
            self.client = FalkorDB(
                host=config.FALKORDB_HOST,
                port=config.FALKORDB_PORT,
                username=config.FALKORDB_USERNAME,
                password=config.FALKORDB_PASSWORD,
            )
        self.graph = self.client.select_graph(config.GRAPH_NAME)
        self._init_indices()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _init_indices(self):
        """Create indices on primary entity identifiers for rapid lookup."""
        indexed_labels = [
            "Employee", "Team", "Project", "Asset", "Document",
            "Agent", "Session", "Interaction", "Concept",
            "Incident", "Tool", "Log"
        ]
        for label in indexed_labels:
            try:
                self.graph.query(f"CREATE INDEX FOR (n:{label}) ON (n.id)")
            except Exception:
                pass

    def query(self, cypher: str, params: Optional[Dict[str, Any]] = None) -> List[List[Any]]:
        """Execute parameterized Cypher query against FalkorDB."""
        res = self.graph.query(cypher, params or {})
        return res.result_set

    def query_dicts(self, cypher: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Execute Cypher query and return rows as dictionaries mapped to header columns."""
        res = self.graph.query(cypher, params or {})
        headers = []
        for col in res.header:
            if isinstance(col, (list, tuple)) and len(col) > 1:
                headers.append(str(col[1]))
            else:
                headers.append(str(col))
        output = []
        for row in res.result_set:
            entry = {}
            for i, col_name in enumerate(headers):
                val = row[i]
                if hasattr(val, "properties"):
                    entry[col_name] = val.properties
                else:
                    entry[col_name] = val
            output.append(entry)
        return output

    def create_node(self, label: str, properties: Dict[str, Any]) -> None:
        """Upsert a node by its 'id' property."""
        cypher = f"MERGE (n:{label} {{id: $id}}) SET n += $props"
        self.query(cypher, {"id": properties["id"], "props": properties})

    def get_node(self, label: str, id_val: Any) -> Optional[Dict[str, Any]]:
        """Fetch a node's properties by ID."""
        cypher = f"MATCH (n:{label} {{id: $id}}) RETURN n LIMIT 1"
        res = self.query(cypher, {"id": id_val})
        if res and len(res) > 0 and len(res[0]) > 0:
            node = res[0][0]
            return node.properties if hasattr(node, "properties") else node
        return None

    def update_node(self, label: str, id_val: Any, updates: Dict[str, Any]) -> None:
        """Update node attributes."""
        cypher = f"MATCH (n:{label} {{id: $id}}) SET n += $updates"
        self.query(cypher, {"id": id_val, "updates": updates})

    def create_edge(
        self,
        from_label: str,
        from_id: Any,
        rel_type: str,
        to_label: str,
        to_id: Any,
        rel_props: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Create a directed edge between two existing nodes."""
        props_str = " SET r += $props" if rel_props else ""
        cypher = f"""
        MATCH (a:{from_label} {{id: $from_id}}), (b:{to_label} {{id: $to_id}})
        MERGE (a)-[r:{rel_type}]->(b)
        {props_str}
        """
        params = {"from_id": from_id, "to_id": to_id}
        if rel_props:
            params["props"] = rel_props
        self.query(cypher, params)

    def get_graph_visualization(self, limit: int = 150) -> Dict[str, Any]:
        """Return nodes and edges formatted for visual graph renderers (Vis.js / Cytoscape)."""
        cypher = f"""
        MATCH (a)-[r]->(b)
        RETURN labels(a)[0] AS a_label, a.id AS a_id, a.name AS a_name, a.title AS a_title,
               type(r) AS rel,
               labels(b)[0] AS b_label, b.id AS b_id, b.name AS b_name, b.title AS b_title
        LIMIT {limit}
        """
        rows = self.query(cypher)
        nodes_dict = {}
        edges = []

        label_colors = {
            "Asset": "#f97316",       # Vibrant Solar Orange
            "Incident": "#ef4444",    # Critical Red
            "Tool": "#fb923c",        # Amber Orange
            "Agent": "#ff6b00",       # Electric Orange
            "Session": "#fdba74",     # Muted Solar
            "Interaction": "#ea580c", # Burnt Orange
            "Concept": "#f59e0b",     # Amber Gold
            "Employee": "#94a3b8",    # Refined Slate
            "Team": "#cbd5e1",        # Platinum
            "Project": "#38bdf8",     # Cyan Accent
            "Document": "#10b981",    # Emerald
            "Log": "#d97706",         # Deep Amber
        }

        for row in rows:
            a_label, a_id, a_name, a_title, rel, b_label, b_id, b_name, b_title = row
            a_display = a_name or a_title or str(a_id)
            b_display = b_name or b_title or str(b_id)

            if a_id not in nodes_dict:
                nodes_dict[a_id] = {
                    "id": a_id,
                    "label": f"{a_label}: {a_display}",
                    "group": a_label,
                    "color": label_colors.get(a_label, "#64748b"),
                }
            if b_id not in nodes_dict:
                nodes_dict[b_id] = {
                    "id": b_id,
                    "label": f"{b_label}: {b_display}",
                    "group": b_label,
                    "color": label_colors.get(b_label, "#64748b"),
                }
            edges.append({
                "from": a_id,
                "to": b_id,
                "label": rel,
                "arrows": "to"
            })

        return {"nodes": list(nodes_dict.values()), "edges": edges}

# Optimized: Graph label indexes ensured on connection initialization.
