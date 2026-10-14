import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

FALKORDB_HOST = os.getenv("FALKORDB_HOST", None)
FALKORDB_PORT = int(os.getenv("FALKORDB_PORT", 6379))
FALKORDB_USERNAME = os.getenv("FALKORDB_USERNAME", None)
FALKORDB_PASSWORD = os.getenv("FALKORDB_PASSWORD", None)
GRAPH_NAME = os.getenv("FALKORDB_GRAPH_NAME", "scout_enterprise")

# If no remote host is configured, we use the embedded FalkorDB engine
USE_EMBEDDED = FALKORDB_HOST is None or FALKORDB_HOST.strip() == ""
DB_PATH = os.getenv("SCOUT_DB_PATH", str(BASE_DIR / "data" / "scout_falkor.db"))
