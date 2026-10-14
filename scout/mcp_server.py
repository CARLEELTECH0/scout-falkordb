"""
Model Context Protocol (MCP) Server for Scout
Exposes FalkorDB graph reasoning tools directly to Claude Code, Hermes, Antigravity, and other agent harnesses.
"""

import sys
import json
from scout.db import FalkorGraph
from scout.brain import CompanyBrain
from scout.memory import AgentMemory
from scout.agent import ScoutActionAgent

TOOLS_SPEC = [
    {
        "name": "scout_compute_blast_radius",
        "description": "Compute multi-hop organizational blast radius if a target server or database is compromised.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "asset_id": {"type": "string", "description": "Asset ID, e.g. AST-01 (prod-auth-gateway), AST-02 (prod-falcon-cluster)"}
            },
            "required": ["asset_id"]
        }
    },
    {
        "name": "scout_investigate_incident",
        "description": "Run autonomous multi-hop investigation across FalkorDB topology for an incident.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "incident_id": {"type": "string", "description": "Incident ID, e.g. INC-2026-001"}
            },
            "required": ["incident_id"]
        }
    },
    {
        "name": "scout_recall_memory",
        "description": "Recall past solutions and semantic concepts from agent graph memory.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "concept": {"type": "string", "description": "Concept keyword, e.g. 'BruteForceSpike', 'PrivilegeEscalation'"}
            },
            "required": ["concept"]
        }
    },
    {
        "name": "scout_audit_access_path",
        "description": "Audit multi-hop relationship path between an employee and a target infrastructure asset.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "employee_id": {"type": "string", "description": "Employee ID, e.g. EMP-02"},
                "asset_id": {"type": "string", "description": "Asset ID, e.g. AST-01"}
            },
            "required": ["employee_id", "asset_id"]
        }
    },
    {
        "name": "scout_quarantine_asset",
        "description": "Quarantine a compromised server or database to isolate it from the enterprise graph.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "asset_id": {"type": "string", "description": "Asset ID to isolate"},
                "reason": {"type": "string", "description": "Security rationale for quarantine"}
            },
            "required": ["asset_id", "reason"]
        }
    }
]

def handle_call(name: str, args: dict) -> dict:
    db = FalkorGraph.get_instance()
    brain = CompanyBrain(db)
    memory = AgentMemory(db)
    agent = ScoutActionAgent(db=db)

    if name == "scout_compute_blast_radius":
        return brain.compute_blast_radius(args["asset_id"])
    elif name == "scout_investigate_incident":
        return agent.investigate_incident(args["incident_id"])
    elif name == "scout_recall_memory":
        return {"recalled": memory.recall_procedural_memory(args["concept"])}
    elif name == "scout_audit_access_path":
        return {"paths": brain.audit_access_path(args["employee_id"], args["asset_id"])}
    elif name == "scout_quarantine_asset":
        return agent.quarantine_asset(args["asset_id"], args["reason"])
    else:
        raise ValueError(f"Unknown tool: {name}")

def main():
    """Stdio JSON-RPC loop for Model Context Protocol."""
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            req_id = req.get("id")

            if method == "tools/list":
                res = {"jsonrpc": "2.0", "id": req_id, "result": {"tools": TOOLS_SPEC}}
            elif method == "tools/call":
                params = req.get("params", {})
                tool_name = params.get("name")
                tool_args = params.get("arguments", {})
                result_data = handle_call(tool_name, tool_args)
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(result_data, indent=2)}]
                    }
                }
            else:
                res = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_res = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            sys.stdout.write(json.dumps(err_res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
