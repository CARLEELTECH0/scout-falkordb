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
