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
