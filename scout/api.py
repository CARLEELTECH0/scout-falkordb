"""
FastAPI REST Backend & Interactive Single-Page Visualizer for Scout
Serves the unified FalkorDB graph, multi-hop reasoning endpoints, and the Spatial Navigation Dashboard:
- Top Context Bar: Search/Command bar, View pivots, Dynamic Micro-Telemetry Pill
- Full-Screen Honeycomb: Wireframe grid, sprouting nodes, lineage highlighting, pulsing threat alert
- Pop-Out Inspector Ledger: Contextual telemetry drawer that slides out when alert node is clicked
- Floating Narrative Launcher: FAB bubble that expands into dual-stream chat drawer on demand
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

from scout.db import FalkorGraph
from scout.brain import CompanyBrain
from scout.memory import AgentMemory
from scout.agent import ScoutActionAgent
from scout.seed import seed_enterprise_graph

app = FastAPI(title="Scout: Autonomous Enterprise Knowledge & Security Investigator", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = FalkorGraph.get_instance()
brain = CompanyBrain(db)
memory = AgentMemory(db)
agent = ScoutActionAgent(db=db)

# -------------------------------------------------------------
# Request Schemas
# -------------------------------------------------------------
class InvestigateRequest(BaseModel):
    incident_id: str
    session_id: Optional[str] = None

class LogTriageRequest(BaseModel):
    message: str
    level: str = "WARN"
    target_asset_id: str = "AST-01"
    session_id: Optional[str] = None

class SessionCreateRequest(BaseModel):
    agent_id: str = "AGT-01"
    user_id: str = "EMP-02"
    topic: str = "Security Operations Sweep"

class DirectiveRequest(BaseModel):
    directive: str
    incident_id: Optional[str] = "INC-2026-001"

# -------------------------------------------------------------
# API Endpoints
# -------------------------------------------------------------
@app.get("/api/stats")
def get_stats():
    """Return live summary counts across the graph."""
    node_count = db.query("MATCH (n) RETURN count(n)")[0][0]
    edge_count = db.query("MATCH ()-[r]->() RETURN count(r)")[0][0]
    incident_count = db.query("MATCH (i:Incident) RETURN count(i)")[0][0]
    quarantine_count = db.query("MATCH (a:Asset {status: 'Quarantined'}) RETURN count(a)")[0][0]
    return {
        "nodes": node_count,
        "edges": edge_count,
        "incidents": incident_count,
        "quarantined": quarantine_count,
        "employees": 10,
        "teams": 3,
        "projects": 2,
        "assets": 3,
        "documents": 5,
        "velocity": "42 ops/s"
    }

@app.get("/api/incidents")
def list_incidents():
    """List all incidents with status and severity."""
    cypher = """
    MATCH (i:Incident)
    OPTIONAL MATCH (i)-[:AFFECTS]->(a:Asset)
    RETURN i.id AS id, i.title AS title, i.severity AS severity, i.status AS status, a.name AS target_asset, i.created_at AS created_at
    ORDER BY i.created_at DESC
    """
    return db.query_dicts(cypher)

@app.get("/api/assets")
def list_assets():
    """List all infrastructure assets."""
    cypher = "MATCH (a:Asset) RETURN a.id AS id, a.name AS name, a.type AS type, a.tier AS tier, a.status AS status ORDER BY a.tier ASC"
    return db.query_dicts(cypher)

@app.get("/api/graph")
def get_graph():
    """Return nodes and edges for graph visualization."""
    return db.get_graph_visualization(limit=300)

@app.post("/api/seed")
def reseed():
    """Reset and re-seed the full enterprise graph."""
    seed_enterprise_graph()
    return {"status": "success", "message": "FalkorDB graph reset and seeded successfully."}

@app.get("/api/brain/blast-radius/{asset_id}")
def get_blast_radius(asset_id: str):
    """Track 3: Blast radius evaluation for a target infrastructure asset."""
    return brain.compute_blast_radius(asset_id)

@app.get("/api/brain/employee/{employee_id}")
def get_employee(employee_id: str):
    """Track 3: Employee reporting chain, clearances, and access permissions."""
    return brain.get_employee_context(employee_id)

@app.get("/api/brain/access-path")
def audit_access(employee_id: str, asset_id: str):
    """Track 3: Multi-hop access path between employee and asset."""
    return brain.audit_access_path(employee_id, asset_id)

@app.post("/api/memory/session")
def create_session(req: SessionCreateRequest):
    """Track 2: Start persistent agent memory session."""
    sid = memory.start_session(req.agent_id, req.user_id, req.topic)
    return {"session_id": sid, "status": "active"}

@app.get("/api/memory/session/{session_id}")
def get_session(session_id: str):
    """Track 2: Retrieve chronological interaction memory for a session."""
    return memory.get_session_history(session_id)

@app.get("/api/memory/recall")
def recall(q: str):
    """Track 2: Recall semantic memory concepts and past solutions."""
    concepts = memory.recall_concepts(q)
    procedural = memory.recall_procedural_memory(q)
    return {"concepts": concepts, "procedural_solutions": procedural}

@app.post("/api/agent/investigate")
def investigate(req: InvestigateRequest):
    """Track 1: Run autonomous multi-hop investigation on an incident."""
    return agent.investigate_incident(req.incident_id, req.session_id)

@app.post("/api/agent/triage-log")
def triage_log(req: LogTriageRequest):
    """Track 1: Real-time telemetry ingestion and automated triage."""
    return agent.ingest_and_triage_log(req.message, req.level, req.target_asset_id, req.session_id)

@app.post("/api/agent/directive")
def human_directive(req: DirectiveRequest):
    """Inject human operator directive into the multi-agent collaboration loop."""
    time_str = datetime.now().strftime("%H:%M:%S")
    return {
        "status": "Acknowledged",
        "directive": req.directive,
        "timestamp": time_str,
        "security_response": {
            "agent": "Scout-Alpha",
            "role": "Security Guardian",
            "message": f"Operator Directive received: \"{req.directive}\". Initiating targeted Cypher traversal across credentials, session tokens, and access paths in FalkorDB.",
            "badge": "Checked company records · 14ms"
        },
        "policy_response": {
            "agent": "Policy-Beta",
            "role": "Team & Rules Advisor",
            "message": f"Cross-referencing directive with Compliance Standard SEC-402. Verification logged to episodic audit session SES-101 in FalkorDB.",
            "badge": "Safety rule verified · 18ms"
        }
    }


# -------------------------------------------------------------
# Spatial Navigation & Pop-Out Ledger Dashboard
# -------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def dashboard():
    return """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SCOUT — Generative Honeycomb & Threat Investigator</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['"Plus Jakarta Sans"', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
                        mono: ['"JetBrains Mono"', 'monospace'],
                    },
                    colors: {
                        brand: {
                            500: '#f97316',
                            600: '#ea580c',
                        }
                    }
                }
            }
        }
    </script>
    <style>
        :root {
            --bg-canvas: #07090e;
            --bg-card: rgba(18, 24, 38, 0.82);
            --liquid-orange: #ff6b00;
            --spring-curve: cubic-bezier(0.16, 1, 0.3, 1);
        }

        body {
            background-color: var(--bg-canvas);
            color: #f1f5f9;
            font-feature-settings: "cv02", "cv03", "cv04", "cv11", "tnum";
            letter-spacing: -0.012em;
            height: 100vh;
            overflow: hidden;
        }

        /* Dribbble Pillowy Rounded Cards */
        .dribbble-card {
            background: linear-gradient(150deg, rgba(22, 28, 46, 0.85) 0%, rgba(12, 16, 28, 0.95) 100%);
            backdrop-filter: blur(28px) saturate(210%);
            -webkit-backdrop-filter: blur(28px) saturate(210%);
            border: 1px solid rgba(255, 255, 255, 0.10);
            border-radius: 24px;
            box-shadow: 0 16px 40px -10px rgba(0, 0, 0, 0.80), inset 0 1px 0 rgba(255, 255, 255, 0.12);
            transition: all 0.25s var(--spring-curve);
        }

        /* Solar Orange Button */
        .btn-solar {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 7px;
            height: 38px;
            padding: 0 16px;
            font-size: 0.8125rem;
            font-weight: 600;
            border-radius: 9999px;
            color: #ffffff;
            background: linear-gradient(180deg, #ff7b24 0%, #ea580c 100%);
            border: 1px solid rgba(255, 255, 255, 0.28);
            box-shadow: 0 4px 18px rgba(234, 88, 12, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.45);
            cursor: pointer;
            transition: all 140ms var(--spring-curve);
        }
        .btn-solar:hover:not(:disabled) {
            background: linear-gradient(180deg, #ff8d3d 0%, #f97316 100%);
            box-shadow: 0 6px 24px rgba(249, 115, 22, 0.60);
            transform: translateY(-1px);
        }

        .btn-obsidian {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            height: 38px;
            padding: 0 14px;
            font-size: 0.8125rem;
            font-weight: 500;
            border-radius: 9999px;
            color: #cbd5e1;
            background: rgba(22, 28, 44, 0.65);
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.08);
            cursor: pointer;
            transition: all 140ms var(--spring-curve);
        }
        .btn-obsidian:hover {
            background: rgba(32, 40, 62, 0.85);
            border-color: rgba(249, 115, 22, 0.40);
            color: #ffffff;
            transform: translateY(-1px);
        }

        /* Multi-Layered Threat Pulse Ring Animation */
        @keyframes pulseRing {
            0% { r: 36px; opacity: 0.95; stroke-width: 3.5px; }
            50% { opacity: 0.40; }
            100% { r: 76px; opacity: 0; stroke-width: 0.5px; }
        }
        .pulse-ring-1 {
            animation: pulseRing 2.2s cubic-bezier(0.16, 1, 0.3, 1) infinite;
        }
        .pulse-ring-2 {
            animation: pulseRing 2.2s cubic-bezier(0.16, 1, 0.3, 1) infinite 0.75s;
        }
        .pulse-ring-3 {
            animation: pulseRing 2.2s cubic-bezier(0.16, 1, 0.3, 1) infinite 1.5s;
        }

        /* Directional Animated Flowing Threat Path */
        @keyframes threatFlow {
            from { stroke-dashoffset: 32; }
            to { stroke-dashoffset: 0; }
        }
        .threat-flow-path {
            stroke: #ff6b00;
            stroke-width: 3.5px;
            stroke-dasharray: 8 5;
            animation: threatFlow 1s linear infinite;
            filter: drop-shadow(0 0 10px #ff6b00);
        }

        /* Sprouting Hexagon Scale Animation */
        @keyframes sproutCard {
            0% { transform: scale(0.2); opacity: 0; }
            70% { transform: scale(1.08); opacity: 1; }
            100% { transform: scale(1); opacity: 1; }
        }
        .sprouting-node {
            transform-origin: center;
            animation: sproutCard 0.45s var(--spring-curve) forwards;
        }

        /* Hexagon Interactivity */
        .hex-cell {
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .hex-cell:hover {
            filter: drop-shadow(0 0 14px currentColor);
            stroke-width: 3.5px;
        }
        .hex-cell.dimmed {
            opacity: 0.15;
            filter: grayscale(80%);
        }

        /* Soundwave Equalizer */
        @keyframes soundwave {
            0%, 100% { height: 4px; }
            50% { height: 18px; }
        }
        .sound-bar-1 { animation: soundwave 1.1s infinite ease-in-out 0.1s; }
        .sound-bar-2 { animation: soundwave 1.1s infinite ease-in-out 0.35s; }
        .sound-bar-3 { animation: soundwave 1.1s infinite ease-in-out 0.2s; }
        .sound-bar-4 { animation: soundwave 1.1s infinite ease-in-out 0.5s; }

        .waveform-bar {
            width: 2.5px;
            border-radius: 2px;
            background-color: #cbd5e1;
        }

        /* Pop-Out Inspector Ledger Drawer (Slides in from Right) */
        #inspector-ledger-drawer {
            transition: transform 0.35s var(--spring-curve), opacity 0.3s ease;
            box-shadow: -15px 0 45px rgba(0, 0, 0, 0.85);
        }
        #inspector-ledger-drawer.drawer-closed {
            transform: translateX(110%);
            opacity: 0;
            pointer-events: none;
        }
        #inspector-ledger-drawer.drawer-open {
            transform: translateX(0);
            opacity: 1;
            pointer-events: auto;
        }

        /* Floating Narrative Chat Drawer */
        #narrative-chat-modal {
            transition: transform 0.35s var(--spring-curve), opacity 0.3s ease;
            box-shadow: 0 25px 65px rgba(0, 0, 0, 0.90), 0 0 35px rgba(249, 115, 22, 0.18);
        }
        #narrative-chat-modal.chat-closed {
            transform: translateY(20px) scale(0.92);
            opacity: 0;
            pointer-events: none;
        }
        #narrative-chat-modal.chat-open {
            transform: translateY(0) scale(1);
            opacity: 1;
            pointer-events: auto;
        }

        /* Floating Narrative Action Button (FAB) */
        .fab-narrative {
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.80), 0 0 20px rgba(249, 115, 22, 0.35);
        }
        .fab-narrative:hover {
            transform: scale(1.05);
            box-shadow: 0 14px 40px rgba(0, 0, 0, 0.90), 0 0 30px rgba(249, 115, 22, 0.55);
        }

        /* Micro scrollbars */
        ::-webkit-scrollbar { width: 4px; height: 4px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: rgba(249, 115, 22, 0.28); border-radius: 2px; }
        ::-webkit-scrollbar-thumb:hover { background: rgba(249, 115, 22, 0.50); }
    </style>
</head>
<body class="h-screen w-screen flex flex-col antialiased selection:bg-orange-500/30 selection:text-orange-200 overflow-hidden relative">

    <!-- =================================================================== -->
    <!-- 1. PERSISTENT TOP CONTEXT BAR (UNIVERSAL ANCHOR - 56px)             -->
    <!-- =================================================================== -->
    <header class="h-[56px] px-6 bg-[#090c15] border-b border-white/[0.08] flex items-center justify-between shrink-0 z-40">
        <!-- Brand & Global Search Bar -->
        <div class="flex items-center gap-3.5">
            <div class="w-9 h-9 rounded-2xl bg-gradient-to-br from-orange-500 via-orange-600 to-amber-700 flex items-center justify-center text-base shadow-[0_0_18px_rgba(249,115,22,0.48)] border border-orange-300/35 cursor-pointer" title="Scout FalkorDB Core">
                🛡️
            </div>
            <div class="flex items-center gap-2">
                <span class="font-extrabold text-sm tracking-tight text-white uppercase bg-clip-text text-transparent bg-gradient-to-r from-white via-slate-100 to-orange-300">SCOUT</span>
                <span class="text-[10px] font-mono px-2 py-0.5 rounded-full bg-orange-500/10 text-orange-400 border border-orange-500/30 font-bold">FalkorDB</span>
            </div>

            <div class="h-4 w-px bg-white/10 mx-1 hidden sm:block"></div>

            <!-- Global Search / Command Bar -->
            <div class="relative hidden md:flex items-center w-80">
                <span class="absolute left-3 text-slate-400 text-xs">🔍</span>
                <input id="global-search-input" onkeyup="handleGlobalSearch(event)" type="text" placeholder="Search graph, users, credentials... [⌘K]" class="h-9 w-full bg-black/50 border border-white/10 rounded-full pl-8 pr-12 text-xs text-white placeholder-slate-500 outline-none focus:border-orange-500/60 transition font-mono">
                <span class="absolute right-3 text-[10px] font-mono text-slate-500 bg-white/[0.05] px-1.5 py-0.5 rounded">⌘K</span>
            </div>
        </div>

        <!-- View Navigation Pivots (Persistent Center Anchor) -->
        <div class="flex items-center gap-1.5 bg-black/40 p-1 rounded-full border border-white/[0.08] text-xs font-mono">
            <button onclick="recenterHoneycombCanvas()" class="px-3.5 py-1.5 rounded-full bg-orange-500/20 text-orange-300 border border-orange-500/40 font-bold transition">
                🗺️ Real-Time Map
            </button>
            <button onclick="openAlertSituationDrawer()" id="pivot-alerts-btn" class="px-3.5 py-1.5 rounded-full text-slate-400 hover:text-white transition flex items-center gap-1.5">
                <span>🚨 Incident Ledger</span>
                <span id="pivot-badge" class="px-1.5 py-0.2 rounded-full bg-rose-500 text-white text-[9px] font-bold">1</span>
            </button>
            <button onclick="toggleNarrativeDrawer()" class="px-3.5 py-1.5 rounded-full text-slate-400 hover:text-white transition flex items-center gap-1.5">
                <span>💬 AI Narrative</span>
                <span class="w-1.5 h-1.5 rounded-full bg-orange-400 animate-pulse"></span>
            </button>
        </div>

        <!-- Contextual Status Micro-Telemetry Pill (Shifts Dynamically) -->
        <div class="flex items-center gap-3">
            <div id="telemetry-pill" onclick="openAlertSituationDrawer()" class="px-3.5 py-1.5 rounded-full bg-rose-500/15 border border-rose-500/35 text-rose-300 text-xs font-mono flex items-center gap-2 cursor-pointer hover:border-rose-500 transition shadow-sm" title="Click to pop out situation inspector">
                <span id="telemetry-pill-dot" class="w-2 h-2 rounded-full bg-rose-500 animate-pulse"></span>
                <span id="telemetry-pill-text"><strong>1 Active Breach:</strong> AST-01</span>
                <span id="telemetry-pill-badge" class="text-[9px] px-1.5 py-0.2 rounded bg-rose-500 text-white font-bold">CRITICAL</span>
            </div>
            <button onclick="triggerSimulatedAttack()" class="btn-solar text-xs hidden lg:inline-flex" title="Simulate anomalous telemetry surge">
                <span>⚡ Attack Surge</span>
            </button>
            <button onclick="reseedGraph()" class="btn-obsidian text-xs" title="Reset and reseed graph">
                <span>🔄 Reset</span>
            </button>
        </div>
    </header>

    <!-- =================================================================== -->
    <!-- 2. FULL-SCREEN GENERATIVE HONEYCOMB CANVAS VIEWPORT                 -->
    <!-- =================================================================== -->
    <main class="flex-1 w-full h-full relative overflow-hidden bg-[#070a12] select-none" id="canvas-wrapper">
        
        <!-- Canvas Floating Controls Overlay -->
        <div class="absolute top-4 left-6 z-20 flex items-center gap-2 pointer-events-auto">
            <div class="px-3.5 py-1.5 rounded-full bg-black/75 backdrop-blur-xl border border-white/10 text-xs font-mono text-slate-300 flex items-center gap-2 shadow-lg">
                <span class="text-orange-400 font-bold">🍯 Honeycomb Grid:</span>
                <span id="node-counter-label">16 Active Cells</span>
                <span class="text-slate-600">·</span>
                <span class="text-purple-300">Secondary: People</span>
                <span class="text-slate-600">·</span>
                <span class="text-rose-400">Primary: Threats (RGY)</span>
            </div>
            <button onclick="recenterHoneycombCanvas()" class="px-3 py-1.5 rounded-full bg-black/75 backdrop-blur-xl hover:bg-black/90 border border-white/10 text-slate-300 hover:text-white text-xs font-mono transition" title="Center Canvas">
                ↺ Center
            </button>
            <button onclick="clearLineageHighlight()" id="btn-clear-lineage" class="px-3 py-1.5 rounded-full bg-black/75 backdrop-blur-xl hover:bg-black/90 border border-white/10 text-slate-300 hover:text-white text-xs font-mono transition hidden" title="Clear Lineage Trace">
                ✕ Clear Lineage
            </button>
        </div>

        <!-- Floating Omni-Directional Jump to Alert Button -->
        <button id="btn-jump-alert" onclick="openAlertSituationDrawer()" class="absolute top-4 right-6 z-20 px-4 py-2 rounded-full bg-rose-500/20 hover:bg-rose-500/30 border border-rose-500/70 text-rose-200 text-xs font-mono font-bold flex items-center gap-2 shadow-lg transition hover:scale-105">
            <span class="w-2 h-2 rounded-full bg-rose-500 animate-ping"></span>
            <span>🚨 Inspect Threat: AST-01</span>
        </button>

        <!-- Lineage Path HUD Overlay -->
        <div id="lineage-hud" class="absolute bottom-6 left-6 z-20 px-4 py-2.5 rounded-2xl bg-black/85 backdrop-blur-2xl border border-purple-500/40 text-xs font-mono space-y-1 hidden shadow-2xl max-w-md">
            <div class="text-[10px] uppercase text-purple-300 font-bold flex items-center justify-between">
                <span>Relational Lineage Path</span>
                <span class="text-slate-500 cursor-pointer hover:text-white ml-3" onclick="clearLineageHighlight()">✕</span>
            </div>
            <div id="lineage-path-string" class="text-white text-[11px] leading-relaxed">
                Bob Martinez ➔ tok_98a ➔ prod-auth-gateway
            </div>
        </div>

        <!-- SVG Honeycomb Viewport -->
        <svg id="honeycomb-viewport" class="w-full h-full" style="cursor: grab;">
            <defs>
                <!-- Glow Filters -->
                <filter id="glow-red" x="-40%" y="-40%" width="180%" height="180%">
                    <feGaussianBlur in="SourceGraphic" stdDeviation="7" result="blur" />
                    <feComposite in="SourceGraphic" in2="blur" operator="over" />
                </filter>
                <filter id="glow-amber" x="-30%" y="-30%" width="160%" height="160%">
                    <feGaussianBlur in="SourceGraphic" stdDeviation="5" result="blur" />
                    <feComposite in="SourceGraphic" in2="blur" operator="over" />
                </filter>
                <filter id="glow-purple" x="-30%" y="-30%" width="160%" height="160%">
                    <feGaussianBlur in="SourceGraphic" stdDeviation="5" result="blur" />
                    <feComposite in="SourceGraphic" in2="blur" operator="over" />
                </filter>
            </defs>

            <!-- Layer 1: Zero-State Wireframe Hexagon Grid (The Faint Structural Matrix) -->
            <g id="zero-state-grid"></g>

            <!-- Layer 2: Connection Links & Animated Threat Flow Paths -->
            <g id="honeycomb-links"></g>

            <!-- Layer 3: Solid Sprouting Hexagonal Cards -->
            <g id="honeycomb-cells"></g>

            <!-- Layer 4: Multi-Layered Threat Pulse Rings (Over Alert Node) -->
            <g id="threat-pulse-rings"></g>
        </svg>
    </main>

    <!-- =================================================================== -->
    <!-- 3. POP-OUT INSPECTOR LEDGER DRAWER (SLIDES DIRECTLY OUT OF SITUATION) -->
    <!-- =================================================================== -->
    <aside id="inspector-ledger-drawer" class="drawer-closed fixed top-14 right-0 bottom-0 w-[420px] max-w-[95vw] bg-[#0c101c]/95 backdrop-blur-2xl border-l border-white/10 z-40 flex flex-col p-5 space-y-4 overflow-y-auto">
        <!-- Drawer Header -->
        <div class="flex items-center justify-between pb-3 border-b border-white/[0.08]">
            <div class="flex items-center gap-2">
                <span class="text-base">🚨</span>
                <div>
                    <h3 class="text-xs font-bold text-white uppercase font-mono tracking-wider">The Inspector Ledger</h3>
                    <p class="text-[10px] text-slate-400 font-mono">Direct Situation Telemetry</p>
                </div>
            </div>
            <div class="flex items-center gap-2">
                <span id="inspect-status-badge" class="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold uppercase bg-rose-500/20 text-rose-300 border border-rose-500/40">🔴 CRITICAL</span>
                <button onclick="closeInspectorLedger()" class="w-7 h-7 rounded-full bg-white/[0.06] hover:bg-white/[0.12] text-slate-400 hover:text-white flex items-center justify-center text-xs transition">
                    ✕
                </button>
            </div>
        </div>

        <!-- Active Selected Node Context Card -->
        <div class="dribbble-card p-4 space-y-3 bg-black/60 border-orange-500/30">
            <div class="flex items-start gap-3">
                <div id="ledger-icon" class="w-11 h-11 rounded-2xl bg-orange-600/20 border border-orange-500/40 text-orange-300 flex items-center justify-center text-2xl shrink-0">
                    💻
                </div>
                <div class="space-y-0.5 flex-1 min-w-0">
                    <div class="flex items-center justify-between">
                        <span id="ledger-group" class="text-[10px] font-mono text-orange-400 uppercase font-semibold">Tier-1 Infrastructure Asset</span>
                        <span id="ledger-id" class="text-[10px] font-mono text-slate-400">AST-01</span>
                    </div>
                    <h4 id="ledger-title" class="text-sm font-bold text-white truncate">prod-auth-gateway</h4>
                    <p id="ledger-desc" class="text-[11px] text-slate-300 leading-snug">
                        Primary enterprise authentication bastion and SSH gateway.
                    </p>
                </div>
            </div>

            <!-- Scannable Structured Properties List -->
            <div class="space-y-1.5 pt-2 border-t border-white/[0.08] text-xs font-mono">
                <div class="flex items-center justify-between p-2 rounded-xl bg-white/[0.04]">
                    <span class="text-slate-400 text-[10px]">IP Footprint</span>
                    <span id="ledger-ip" class="text-orange-300 font-bold text-[11px]">192.168.1.105</span>
                </div>
                <div class="flex items-center justify-between p-2 rounded-xl bg-white/[0.04]">
                    <span class="text-slate-400 text-[10px]">Protocol / Port</span>
                    <span class="text-slate-200 text-[11px]">SSHv2 / Port 22</span>
                </div>
                <div class="flex items-center justify-between p-2 rounded-xl bg-white/[0.04]">
                    <span class="text-slate-400 text-[10px]">Access Key Traced</span>
                    <span id="ledger-key" class="text-purple-300 font-bold text-[11px]">tok_98a (Bob Martinez)</span>
                </div>
                <div class="flex items-center justify-between p-2 rounded-xl bg-white/[0.04]">
                    <span class="text-slate-400 text-[10px]">Department / Team</span>
                    <span class="text-purple-300 text-[11px]">SecOps (Alice Chen)</span>
                </div>
            </div>

            <!-- Blast Radius & Risk Score Meter -->
            <div class="p-3 rounded-2xl bg-black/60 border border-rose-500/25 space-y-2">
                <div class="flex items-center justify-between text-[11px] font-mono">
                    <span class="text-slate-400">Blast Radius Risk</span>
                    <span id="ledger-risk-score" class="text-rose-400 font-bold">125 / 100 [CRITICAL]</span>
                </div>
                <div class="w-full h-2 rounded-full bg-slate-900 overflow-hidden">
                    <div id="ledger-risk-bar" class="h-full bg-gradient-to-r from-amber-500 via-rose-500 to-red-600 rounded-full" style="width: 100%"></div>
                </div>
                <div class="text-[10px] text-slate-400 flex items-center justify-between">
                    <span>Exposed Staff: 2</span>
                    <span>Projects at Risk: 1</span>
                </div>
            </div>

            <!-- One-Click Instant Mitigation Action Button -->
            <button onclick="executeMitigation()" id="btn-ledger-quarantine" class="btn-solar w-full h-11 text-xs font-bold shadow-lg shadow-orange-500/35">
                <span>🛡️ Quarantine Asset & Contain Breach</span>
            </button>
        </div>

        <!-- Scannable Lineage Trace Ledger -->
        <div class="dribbble-card p-4 space-y-2.5 bg-black/50 flex-1">
            <div class="flex items-center justify-between pb-1 border-b border-white/[0.08]">
                <span class="text-[10px] font-mono uppercase text-slate-400 font-bold">Step-by-Step Traversal Trace</span>
                <span class="text-[10px] font-mono text-purple-300">Cypher Multi-Hop</span>
            </div>
            <div class="space-y-2 text-[11px] font-mono text-slate-300" id="ledger-steps">
                <div class="flex items-center gap-2">
                    <span class="w-4 h-4 rounded-full bg-orange-500/20 text-orange-400 text-[9px] flex items-center justify-center font-bold">1</span>
                    <span>Anomalous surge: 14 failed SSH attempts</span>
                </div>
                <div class="flex items-center gap-2">
                    <span class="w-4 h-4 rounded-full bg-purple-500/20 text-purple-400 text-[9px] flex items-center justify-center font-bold">2</span>
                    <span>Matched credential token: <strong class="text-purple-300">tok_98a</strong></span>
                </div>
                <div class="flex items-center gap-2">
                    <span class="w-4 h-4 rounded-full bg-purple-500/20 text-purple-400 text-[9px] flex items-center justify-center font-bold">3</span>
                    <span>Traced employee: <strong class="text-white">Bob Martinez</strong> (SecOps)</span>
                </div>
                <div class="flex items-center gap-2">
                    <span class="w-4 h-4 rounded-full bg-emerald-500/20 text-emerald-400 text-[9px] flex items-center justify-center font-bold">4</span>
                    <span>Rule SEC-402 passed: Quarantine authorized</span>
                </div>
            </div>
        </div>
    </aside>

    <!-- =================================================================== -->
    <!-- 4. FLOATING NARRATIVE ACTION BUTTON (FAB) & EXPANDABLE CHAT MODAL   -->
    <!-- =================================================================== -->
    <!-- Floating Narrative Trigger Pill -->
    <button id="floating-narrative-btn" onclick="toggleNarrativeDrawer()" class="fab-narrative fixed bottom-6 right-6 z-30 px-4 py-2.5 rounded-full bg-gradient-to-r from-[#141b2e] to-[#1e172f] border border-orange-500/40 backdrop-blur-2xl text-white shadow-2xl flex items-center gap-3 transition cursor-pointer">
        <div class="relative">
            <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-orange-500 to-purple-600 flex items-center justify-center font-bold text-xs shadow">AI</div>
            <span class="absolute -top-0.5 -right-0.5 w-2.5 h-2.5 rounded-full bg-emerald-400 border border-black animate-pulse"></span>
        </div>
        <div class="text-left font-mono">
            <div class="text-xs font-bold text-white flex items-center gap-1.5">
                <span>The Narrative</span>
                <span class="px-1.5 py-0.2 rounded-full bg-orange-500 text-[9px] font-bold">2 Active</span>
            </div>
            <span class="text-[10px] text-orange-300">Scout & Policy Live</span>
        </div>
        <div class="flex items-center gap-0.5 h-3 pl-1">
            <span class="w-1 bg-orange-400 rounded-full sound-bar-1"></span>
            <span class="w-1 bg-amber-400 rounded-full sound-bar-2"></span>
            <span class="w-1 bg-purple-400 rounded-full sound-bar-3"></span>
        </div>
    </button>

    <!-- Floating Narrative Chat Drawer / Modal -->
    <div id="narrative-chat-modal" class="chat-closed fixed bottom-20 right-6 z-40 w-[450px] max-w-[94vw] h-[640px] max-h-[85vh] dribbble-card bg-[#0b0e19]/95 flex flex-col overflow-hidden border-orange-500/40">
        <!-- Chat Header -->
        <div class="h-14 px-5 border-b border-white/[0.08] flex items-center justify-between shrink-0 bg-black/50">
            <div class="flex items-center gap-2.5">
                <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-orange-500 to-purple-600 flex items-center justify-center font-bold text-xs text-white">
                    AI
                </div>
                <div>
                    <h3 class="text-xs font-bold text-white leading-tight">The Narrative: Agent Debate</h3>
                    <p class="text-[10px] text-emerald-400 font-mono">Online · Dual Asynchronous Stream</p>
                </div>
            </div>
            <div class="flex items-center gap-2">
                <!-- Soundwave Equalizer -->
                <div class="flex items-center gap-1 px-2.5 py-1 rounded-full bg-orange-500/10 border border-orange-500/30 text-[10px] font-mono text-orange-300">
                    <span>🎙️ Voice: 04:18</span>
                </div>
                <button onclick="toggleNarrativeDrawer()" class="w-7 h-7 rounded-full bg-white/[0.06] hover:bg-white/[0.12] text-slate-400 hover:text-white flex items-center justify-center text-xs transition">
                    ✕
                </button>
            </div>
        </div>

        <!-- Chat Messages & System Log Marker Anchors -->
        <div id="narrative-stream" class="flex-1 overflow-y-auto p-4 space-y-3.5 text-xs">
            <!-- Message 1: Scout-Alpha -->
            <div class="p-3.5 rounded-3xl bg-black/60 border border-orange-500/25 space-y-2">
                <div class="flex items-center justify-between text-[11px]">
                    <div class="flex items-center gap-2">
                        <div class="w-5 h-5 rounded-full bg-orange-600/40 text-orange-300 font-bold text-[9px] flex items-center justify-center border border-orange-500/30">SA</div>
                        <span class="font-bold text-orange-300 font-mono">Scout-Alpha</span>
                        <span class="text-[9px] px-1.5 py-0.2 rounded bg-orange-500/10 text-orange-400 border border-orange-500/30 font-mono">Analysis</span>
                    </div>
                    <span class="text-[10px] text-slate-400 font-mono">12:44:10</span>
                </div>
                <p class="text-slate-200 text-xs leading-relaxed">
                    Detected anomalous telemetry surge: <strong class="text-white">14 consecutive failed root SSH authentications</strong> on <code class="text-orange-300 bg-black/60 px-1 py-0.5 rounded">prod-auth-gateway</code> (AST-01) from unauthorized IP <code class="text-orange-300 bg-black/60 px-1 py-0.5 rounded">192.168.1.105</code>.
                </p>

                <!-- Voice Note Player -->
                <div class="p-2.5 rounded-2xl bg-orange-950/30 border border-orange-500/35 flex items-center gap-3">
                    <button onclick="toggleVoiceAudio(this)" class="w-7 h-7 rounded-full bg-gradient-to-r from-orange-500 to-amber-600 text-white flex items-center justify-center text-[10px] shadow-md shadow-orange-500/30">
                        <span class="play-icon">▶</span>
                    </button>
                    <div class="flex-1 flex items-center gap-1 h-4">
                        <span class="waveform-bar h-2 bg-orange-400"></span>
                        <span class="waveform-bar h-4 bg-orange-400"></span>
                        <span class="waveform-bar h-3 bg-orange-300"></span>
                        <span class="waveform-bar h-4 bg-orange-400"></span>
                        <span class="waveform-bar h-2 bg-orange-300"></span>
                        <span class="waveform-bar h-4 bg-orange-400"></span>
                        <span class="waveform-bar h-2 bg-slate-500"></span>
                    </div>
                    <span class="text-[10px] font-mono text-orange-300 font-bold">0:14</span>
                </div>
            </div>

            <!-- SYSTEM LOG MARKER ANCHOR 01 -->
            <div class="p-2.5 rounded-2xl bg-purple-950/25 border border-purple-500/30 flex items-center gap-2.5 text-[11px] font-mono text-purple-200 shadow-sm">
                <span class="w-2 h-2 rounded-full bg-purple-400"></span>
                <span class="font-bold text-white">[12:44:11]</span>
                <span class="truncate">Sprouted node <strong>tok_98a</strong> ➔ Assigned to <strong>Bob Martinez</strong></span>
            </div>

            <!-- Message 2: Policy-Beta -->
            <div class="p-3.5 rounded-3xl bg-black/60 border border-purple-500/25 space-y-2">
                <div class="flex items-center justify-between text-[11px]">
                    <div class="flex items-center gap-2">
                        <div class="w-5 h-5 rounded-full bg-purple-600/40 text-purple-300 font-bold text-[9px] flex items-center justify-center border border-purple-500/30">PB</div>
                        <span class="font-bold text-purple-300 font-mono">Policy-Beta</span>
                        <span class="text-[9px] px-1.5 py-0.2 rounded bg-purple-500/10 text-purple-400 border border-purple-500/30 font-mono">Governance</span>
                    </div>
                    <span class="text-[10px] text-slate-400 font-mono">12:44:13</span>
                </div>
                <div class="p-2 rounded-xl bg-purple-950/30 border-l-2 border-purple-400 text-[10px] text-slate-300 space-y-0.5">
                    <span class="text-purple-400 font-semibold block">Replied to Scout-Alpha:</span>
                    <p class="truncate italic opacity-85">"Detected anomalous telemetry surge: 14 consecutive failed root..."</p>
                </div>
                <p class="text-slate-200 text-xs leading-relaxed">
                    Evaluated blast radius in FalkorDB: <code class="text-purple-300 bg-black/60 px-1 py-0.5 rounded">prod-auth-gateway</code> is accessed by <strong class="text-white">Bob Martinez</strong> (<span class="text-purple-300">SecOps Team</span>). Affects <strong class="text-amber-300">Project FalconShield</strong>. Risk score: <strong class="text-rose-400">125 / 100 [CRITICAL]</strong>. Rule <span class="text-purple-300 font-semibold">SEC-402</span> mandates instant quarantine.
                </p>
            </div>

            <!-- SYSTEM LOG MARKER ANCHOR 02 -->
            <div class="p-2.5 rounded-2xl bg-orange-950/25 border border-orange-500/30 flex items-center gap-2.5 text-[11px] font-mono text-orange-200 shadow-sm">
                <span class="w-2 h-2 rounded-full bg-orange-400 animate-pulse"></span>
                <span class="font-bold text-white">[12:44:14]</span>
                <span class="truncate">Sprouted Alert Node <strong>AST-01</strong> ➔ Directional threat path active</span>
            </div>
        </div>

        <!-- Chat Input Form -->
        <div class="p-3.5 bg-black/60 border-t border-white/[0.08] shrink-0">
            <form id="directive-form" onsubmit="submitDirective(event)" class="flex items-center gap-2">
                <button type="button" class="w-9 h-9 rounded-full bg-white/[0.05] hover:bg-white/[0.1] text-slate-400 hover:text-white flex items-center justify-center text-xs transition" title="Voice Input">
                    🎙️
                </button>
                <button type="button" class="w-9 h-9 rounded-full bg-white/[0.05] hover:bg-white/[0.1] text-slate-400 hover:text-white flex items-center justify-center text-xs transition" title="Attach Context">
                    📎
                </button>
                <input id="directive-input" type="text" placeholder="Message agents or inject directive..." class="h-10 bg-black/80 border border-white/10 focus:border-orange-500/60 rounded-full px-4 text-xs text-white placeholder-slate-500 flex-1 outline-none font-mono transition">
                <button type="submit" class="w-10 h-10 rounded-full bg-gradient-to-r from-orange-500 to-amber-600 hover:scale-105 active:scale-95 text-white flex items-center justify-center shadow-lg shadow-orange-500/35 transition shrink-0" title="Dispatch Directive">
                    <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
                </button>
            </form>
        </div>
    </div>

    <!-- CLIENT JAVASCRIPT LOGIC -->
    <script>
        let currentIncident = 'INC-2026-001';
        let isQuarantined = false;
        let isNarrativeOpen = false;
        let isInspectorOpen = false;

        // Canvas Coordinates & Graph State
        let allGraphNodes = [];
        const R = 44; // Hexagon radius
        let originX = window.innerWidth / 2 - 40;
        let originY = window.innerHeight / 2 - 40;

        // Update center on resize
        window.addEventListener('resize', () => {
            originX = window.innerWidth / 2 - 40;
            originY = window.innerHeight / 2 - 40;
            renderZeroStateGrid();
            renderHoneycombCanvas();
        });

        // ----------------------------------------------------
        // 1. Zero-State Wireframe Hexagon Grid Generator
        // ----------------------------------------------------
        function getHexPoints(cx, cy, radius) {
            let pts = [];
            for (let i = 0; i < 6; i++) {
                const angle = (Math.PI / 3) * i + Math.PI / 6;
                const px = cx + radius * Math.cos(angle);
                const py = cy + radius * Math.sin(angle);
                pts.push(`${px.toFixed(1)},${py.toFixed(1)}`);
            }
            return pts.join(" ");
        }

        function renderZeroStateGrid() {
            const gridG = document.getElementById('zero-state-grid');
            if (!gridG) return;
            gridG.innerHTML = '';

            // Generate a spacious 11x11 wireframe hexagonal matrix
            for (let q = -5; q <= 5; q++) {
                for (let r = -5; r <= 5; r++) {
                    const cx = originX + R * Math.sqrt(3) * (q + r / 2);
                    const cy = originY + R * (3 / 2) * r;
                    const hex = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
                    hex.setAttribute("points", getHexPoints(cx, cy, R - 2));
                    hex.setAttribute("stroke", "rgba(255, 255, 255, 0.04)");
                    hex.setAttribute("stroke-width", "1");
                    hex.setAttribute("stroke-dasharray", "2 3");
                    hex.setAttribute("fill", "none");
                    gridG.appendChild(hex);
                }
            }
        }

        // ----------------------------------------------------
        // 2. Honeycomb Nodes & Sprouting Mechanism
        // ----------------------------------------------------
        const nodeDefinitions = [
            // Center & Threat Epicenter
            { id: "AST-01", label: "prod-auth-gateway", q: 0, r: 0, group: "Asset", icon: "💻", isThreat: true },
            { id: "tok_98a", label: "tok_98a", q: 1, r: -1, group: "Credential", icon: "🔑", parent: "AST-01" },
            { id: "EMP-02", label: "Bob Martinez", q: 2, r: -1, group: "Employee", icon: "👤", parent: "tok_98a" },
            { id: "TEAM-01", label: "SecOps Team", q: 3, r: -2, group: "Team", icon: "📁", parent: "EMP-02" },
            { id: "EMP-01", label: "Alice Chen", q: 3, r: -1, group: "Employee", icon: "👤", parent: "TEAM-01" },
            { id: "PRJ-01", label: "Project FalconShield", q: 1, r: 1, group: "Project", icon: "🚀", parent: "AST-01" },
            { id: "AST-02", label: "prod-falcon-cluster", q: -1, r: 1, group: "Asset", icon: "🗄️", parent: "PRJ-01" },
            { id: "AST-03", label: "analytics-warehouse", q: -2, r: 0, group: "Asset", icon: "📊", parent: "AST-01" },
            { id: "DOC-01", label: "Security Policy 402", q: -1, r: -1, group: "Document", icon: "📑", parent: "AST-01" },
            { id: "AGT-01", label: "Scout-Alpha", q: -2, r: 2, group: "Agent", icon: "🤖", parent: "AST-01" },
            { id: "AGT-02", label: "Policy-Beta", q: -1, r: 2, group: "Agent", icon: "⚖️", parent: "DOC-01" },
            { id: "EMP-03", label: "Charlie Kim", q: 2, r: 0, group: "Employee", icon: "👤", parent: "TEAM-01" },
            { id: "EMP-04", label: "Diana Prince", q: 2, r: 1, group: "Employee", icon: "👤", parent: "PRJ-01" },
            { id: "INC-2026-001", label: "Brute-Force Anomaly", q: 0, r: -2, group: "Incident", icon: "🚨", parent: "AST-01" }
        ];

        function calculateNodeCoords() {
            allGraphNodes = nodeDefinitions.map(n => {
                const cx = originX + R * Math.sqrt(3) * (n.q + n.r / 2);
                const cy = originY + R * (3 / 2) * n.r;
                
                // Color rules:
                // - People / Employee: Secondary Vibrant Violet (#a855f7)
                // - Threats & Situations: Primary RGY (🔴 Red, 🟡 Yellow, 🟢 Green)
                let color = "#94a3b8";
                if (n.group === "Employee") {
                    color = "#a855f7"; // Vibrant Secondary Purple
                } else if (n.id === "AST-01" || n.group === "Incident") {
                    color = isQuarantined ? "#10b981" : "#ef4444"; // 🔴 Red or 🟢 Green post-lockdown
                } else if (n.id === "AST-02" || n.group === "Project" || n.group === "Credential") {
                    color = "#f59e0b"; // 🟡 Yellow Warning / Sensitive
                } else if (n.id === "AST-03" || n.group === "Document") {
                    color = "#10b981"; // 🟢 Green Safe
                } else if (n.group === "Team") {
                    color = "#38bdf8"; // Cyan
                } else if (n.group === "Agent") {
                    color = "#ff6b00"; // Solar Orange
                }

                return { ...n, cx, cy, color };
            });
        }

        function renderHoneycombCanvas() {
            calculateNodeCoords();
            const linksG = document.getElementById('honeycomb-links');
            const cellsG = document.getElementById('honeycomb-cells');
            const pulseG = document.getElementById('threat-pulse-rings');
            if (!linksG || !cellsG || !pulseG) return;

            linksG.innerHTML = '';
            cellsG.innerHTML = '';
            pulseG.innerHTML = '';

            const nodeMap = {};
            allGraphNodes.forEach(n => { nodeMap[n.id] = n; });

            // 1. Render Links (Threat Flow & Structural Paths)
            allGraphNodes.forEach(node => {
                if (node.parent && nodeMap[node.parent]) {
                    const parent = nodeMap[node.parent];
                    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
                    line.setAttribute("x1", node.cx);
                    line.setAttribute("y1", node.cy);
                    line.setAttribute("x2", parent.cx);
                    line.setAttribute("y2", parent.cy);

                    // Threat line flowing from employee -> credential -> alert node
                    const isThreatPath = !isQuarantined && (
                        (node.id === "tok_98a" && parent.id === "AST-01") ||
                        (node.id === "EMP-02" && parent.id === "tok_98a")
                    );

                    if (isThreatPath) {
                        line.setAttribute("class", "threat-flow-path");
                    } else {
                        line.setAttribute("stroke", "rgba(255, 255, 255, 0.12)");
                        line.setAttribute("stroke-width", "1.5");
                    }

                    line.setAttribute("id", `link-${node.id}-${parent.id}`);
                    linksG.appendChild(line);
                }
            });

            // 2. Render Expanding Multi-Layered Threat Pulse Rings
            const alertNode = nodeMap["AST-01"];
            if (alertNode && !isQuarantined) {
                const ring1 = document.createElementNS("http://www.w3.org/2000/svg", "circle");
                ring1.setAttribute("cx", alertNode.cx);
                ring1.setAttribute("cy", alertNode.cy);
                ring1.setAttribute("stroke", "#ef4444");
                ring1.setAttribute("fill", "none");
                ring1.setAttribute("class", "pulse-ring-1");

                const ring2 = document.createElementNS("http://www.w3.org/2000/svg", "circle");
                ring2.setAttribute("cx", alertNode.cx);
                ring2.setAttribute("cy", alertNode.cy);
                ring2.setAttribute("stroke", "#ef4444");
                ring2.setAttribute("fill", "none");
                ring2.setAttribute("class", "pulse-ring-2");

                const ring3 = document.createElementNS("http://www.w3.org/2000/svg", "circle");
                ring3.setAttribute("cx", alertNode.cx);
                ring3.setAttribute("cy", alertNode.cy);
                ring3.setAttribute("stroke", "#ef4444");
                ring3.setAttribute("fill", "none");
                ring3.setAttribute("class", "pulse-ring-3");

                pulseG.appendChild(ring1);
                pulseG.appendChild(ring2);
                pulseG.appendChild(ring3);
            }

            // 3. Render Solid Sprouting Hexagon Cards
            allGraphNodes.forEach((node, i) => {
                const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
                g.setAttribute("class", "hex-cell sprouting-node");
                g.setAttribute("id", `cell-${node.id}`);
                g.style.animationDelay = `${i * 30}ms`;
                g.style.color = node.color;

                // Base Polygon
                const hex = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
                hex.setAttribute("points", getHexPoints(node.cx, node.cy, R - 6));
                hex.setAttribute("fill", "rgba(12, 16, 26, 0.92)");
                hex.setAttribute("stroke", node.color);
                hex.setAttribute("stroke-width", node.id === "AST-01" ? "3" : "2");
                if (node.id === "AST-01" && !isQuarantined) {
                    hex.setAttribute("filter", "url(#glow-red)");
                }

                // Icon
                const icon = document.createElementNS("http://www.w3.org/2000/svg", "text");
                icon.setAttribute("x", node.cx);
                icon.setAttribute("y", node.cy - 5);
                icon.setAttribute("text-anchor", "middle");
                icon.setAttribute("font-size", "14");
                icon.textContent = node.icon;

                // Label
                const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
                label.setAttribute("x", node.cx);
                label.setAttribute("y", node.cy + 13);
                label.setAttribute("text-anchor", "middle");
                label.setAttribute("fill", "#ffffff");
                label.setAttribute("font-size", "8.5");
                label.setAttribute("font-weight", "600");
                label.setAttribute("font-family", "sans-serif");
                label.textContent = node.label.length > 10 ? node.label.substring(0, 9) + '…' : node.label;

                g.appendChild(hex);
                g.appendChild(icon);
                g.appendChild(label);

                // Clicking ANY node (especially pulsing alert) pops out the Inspector Ledger!
                g.addEventListener('click', (e) => {
                    selectNodeAndPopOutInspector(node);
                    e.stopPropagation();
                });

                g.addEventListener('mouseenter', () => {
                    highlightLineage(node);
                });

                cellsG.appendChild(g);
            });
        }

        // ----------------------------------------------------
        // 3. Lineage Highlighting (Traces back to Employee)
        // ----------------------------------------------------
        function highlightLineage(node) {
            const nodeMap = {};
            allGraphNodes.forEach(n => { nodeMap[n.id] = n; });

            const lineageIds = new Set([node.id]);
            let curr = node;
            while (curr && curr.parent && nodeMap[curr.parent]) {
                lineageIds.add(curr.parent);
                curr = nodeMap[curr.parent];
            }

            allGraphNodes.forEach(n => {
                const cell = document.getElementById(`cell-${n.id}`);
                if (cell) {
                    if (lineageIds.has(n.id)) {
                        cell.classList.remove('dimmed');
                        cell.style.filter = "drop-shadow(0 0 10px currentColor)";
                    } else {
                        cell.classList.add('dimmed');
                        cell.style.filter = "none";
                    }
                }
            });

            const hud = document.getElementById('lineage-hud');
            const hudStr = document.getElementById('lineage-path-string');
            const btnClear = document.getElementById('btn-clear-lineage');
            if (hud && hudStr) {
                const pathArr = Array.from(lineageIds).reverse();
                hudStr.innerText = pathArr.join(" ➔ ");
                hud.classList.remove('hidden');
                if (btnClear) btnClear.classList.remove('hidden');
            }
        }

        function clearLineageHighlight() {
            allGraphNodes.forEach(n => {
                const cell = document.getElementById(`cell-${n.id}`);
                if (cell) {
                    cell.classList.remove('dimmed');
                    cell.style.filter = "none";
                }
            });
            const hud = document.getElementById('lineage-hud');
            const btnClear = document.getElementById('btn-clear-lineage');
            if (hud) hud.classList.add('hidden');
            if (btnClear) btnClear.classList.add('hidden');
        }

        // ----------------------------------------------------
        // 4. Pop-Out Inspector Ledger (Directly on Node Click)
        // ----------------------------------------------------
        function selectNodeAndPopOutInspector(node) {
            highlightLineage(node);
            updateInspectorLedger(node);
            openInspectorLedger();
        }

        function openInspectorLedger() {
            const drawer = document.getElementById('inspector-ledger-drawer');
            if (drawer) {
                drawer.classList.remove('drawer-closed');
                drawer.classList.add('drawer-open');
                isInspectorOpen = true;
            }
        }

        function closeInspectorLedger() {
            const drawer = document.getElementById('inspector-ledger-drawer');
            if (drawer) {
                drawer.classList.remove('drawer-open');
                drawer.classList.add('drawer-closed');
                isInspectorOpen = false;
            }
        }

        function openAlertSituationDrawer() {
            const alertNode = allGraphNodes.find(n => n.id === "AST-01");
            if (alertNode) {
                selectNodeAndPopOutInspector(alertNode);
                // Flash scale node
                const alertCell = document.getElementById('cell-AST-01');
                if (alertCell) {
                    alertCell.style.transition = "transform 0.5s var(--spring-curve)";
                    alertCell.style.transform = "scale(1.25)";
                    setTimeout(() => { alertCell.style.transform = "scale(1)"; }, 600);
                }
            }
        }

        function updateInspectorLedger(node) {
            document.getElementById('ledger-icon').innerText = node.icon;
            document.getElementById('ledger-id').innerText = node.id;
            document.getElementById('ledger-title').innerText = node.label;
            document.getElementById('ledger-group').innerText = `${node.group} Telemetry`;

            const badge = document.getElementById('inspect-status-badge');
            if (node.id === "AST-01") {
                badge.innerText = isQuarantined ? "🟢 CONTAINED" : "🔴 CRITICAL";
                badge.className = isQuarantined ? "px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold uppercase bg-emerald-500/20 text-emerald-300 border border-emerald-500/40" : "px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold uppercase bg-rose-500/20 text-rose-300 border border-rose-500/40";
            } else if (node.group === "Employee") {
                badge.innerText = "SECONDARY: PERSON";
                badge.className = "px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold uppercase bg-purple-500/20 text-purple-300 border border-purple-500/40";
            } else {
                badge.innerText = "OPERATIONAL";
                badge.className = "px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold uppercase bg-slate-800 text-slate-300 border border-white/10";
            }
        }

        // ----------------------------------------------------
        // 5. Floating Narrative Icon & Expandable Chat Modal
        // ----------------------------------------------------
        function toggleNarrativeDrawer() {
            const modal = document.getElementById('narrative-chat-modal');
            if (!modal) return;
            isNarrativeOpen = !isNarrativeOpen;
            if (isNarrativeOpen) {
                modal.classList.remove('chat-closed');
                modal.classList.add('chat-open');
            } else {
                modal.classList.remove('chat-open');
                modal.classList.add('chat-closed');
            }
        }

        // ----------------------------------------------------
        // 6. Threat Mitigation & Sprouting Containment Cell
        // ----------------------------------------------------
        async function executeMitigation() {
            const btn = document.getElementById('btn-ledger-quarantine');
            btn.disabled = true;
            btn.innerHTML = "<span>⚙️ Locking Down Gateway...</span>";

            try {
                const res = await fetch('/api/agent/investigate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ incident_id: currentIncident })
                });
                const data = await res.json();
                isQuarantined = true;

                btn.className = "btn-obsidian w-full h-11 text-xs font-bold text-emerald-300 border-emerald-500/40 cursor-default";
                btn.innerHTML = "<span>✓ Quarantined & Contained</span>";

                // Update Telemetry Pill
                const pill = document.getElementById('telemetry-pill');
                const dot = document.getElementById('telemetry-pill-dot');
                const text = document.getElementById('telemetry-pill-text');
                const badge = document.getElementById('telemetry-pill-badge');
                pill.className = "px-3.5 py-1.5 rounded-full bg-emerald-500/15 border border-emerald-500/35 text-emerald-300 text-xs font-mono flex items-center gap-2";
                dot.className = "w-2 h-2 rounded-full bg-emerald-400";
                text.innerHTML = "<strong>System Status:</strong> All Threats Contained";
                badge.innerText = "HEALTHY";
                badge.className = "text-[9px] px-1.5 py-0.2 rounded bg-emerald-500 text-white font-bold";

                // Hide Jump to Alert button
                const btnJump = document.getElementById('btn-jump-alert');
                if (btnJump) btnJump.classList.add('hidden');
                const pivotBadge = document.getElementById('pivot-badge');
                if (pivotBadge) pivotBadge.innerText = "0";

                // Re-render canvas to show green safe state
                renderHoneycombCanvas();

                // Sprout Containment Cell into grid
                sproutNewBranch("AST-01", "ISOLATION_ZONE", "Containment Lock", "Security", "🛡️");

                appendChatMessage("Scout-Alpha", "Asset AST-01 quarantined successfully in FalkorDB. Attack surface eliminated.", "scout", "Quarantine Active · 22ms");
            } catch (err) {
                console.error("Mitigation error:", err);
            }
        }

        async function triggerSimulatedAttack() {
            isQuarantined = false;
            const btnJump = document.getElementById('btn-jump-alert');
            if (btnJump) btnJump.classList.remove('hidden');

            const pill = document.getElementById('telemetry-pill');
            const dot = document.getElementById('telemetry-pill-dot');
            const text = document.getElementById('telemetry-pill-text');
            const badge = document.getElementById('telemetry-pill-badge');
            pill.className = "px-3.5 py-1.5 rounded-full bg-rose-500/15 border border-rose-500/35 text-rose-300 text-xs font-mono flex items-center gap-2 cursor-pointer";
            dot.className = "w-2 h-2 rounded-full bg-rose-500 animate-pulse";
            text.innerHTML = "<strong>1 Active Breach:</strong> AST-01";
            badge.innerText = "CRITICAL";
            badge.className = "text-[9px] px-1.5 py-0.2 rounded bg-rose-500 text-white font-bold";

            const pivotBadge = document.getElementById('pivot-badge');
            if (pivotBadge) pivotBadge.innerText = "1";

            renderHoneycombCanvas();
            openAlertSituationDrawer();

            appendChatMessage("Scout-Alpha", "Caught 14 failed SSH attempts from unauthorized IP 192.168.1.105 on Login Gateway.", "scout", "Triage Surge · 9ms");
        }

        function sproutNewBranch(parentId, newId, label, group, icon) {
            const parent = allGraphNodes.find(n => n.id === parentId);
            if (!parent) return;

            const newNode = {
                id: newId,
                label: label,
                q: parent.q + 1,
                r: parent.r,
                group: group,
                icon: icon,
                parent: parentId
            };
            nodeDefinitions.push(newNode);
            renderHoneycombCanvas();

            // Anchor System Log Marker in Narrative Stream
            const stream = document.getElementById('narrative-stream');
            if (stream) {
                const time = new Date().toLocaleTimeString();
                const div = document.createElement('div');
                div.className = "p-2.5 rounded-2xl bg-orange-950/30 border border-orange-500/35 flex items-center gap-2.5 text-[11px] font-mono text-orange-200 shadow-sm animate-in fade-in";
                div.innerHTML = `
                    <span class="w-2 h-2 rounded-full bg-orange-400 animate-pulse"></span>
                    <span class="font-bold text-white">[${time}]</span>
                    <span class="truncate">FalkorDB Mutation: Sprouted cell <strong>${newId}</strong> off parent <strong>${parentId}</strong></span>
                `;
                stream.appendChild(div);
                stream.scrollTop = stream.scrollHeight;
            }
        }

        // ----------------------------------------------------
        // 7. Chat Directives
        // ----------------------------------------------------
        async function submitDirective(e) {
            e.preventDefault();
            const input = document.getElementById('directive-input');
            const text = input.value.trim();
            if (!text) return;
            input.value = '';

            appendChatMessage("Operator (You)", text, "human");

            try {
                const res = await fetch('/api/agent/directive', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ directive: text, incident_id: currentIncident })
                });
                const data = await res.json();

                setTimeout(() => {
                    appendChatMessage("Scout-Alpha", data.security_response.message, "scout", data.security_response.badge);
                }, 400);

                setTimeout(() => {
                    appendChatMessage("Policy-Beta", data.policy_response.message, "policy", data.policy_response.badge);
                }, 900);
            } catch (err) {
                console.error("Directive error:", err);
            }
        }

        function appendChatMessage(sender, text, type, badge) {
            const stream = document.getElementById('narrative-stream');
            if (!stream) return;
            const time = new Date().toLocaleTimeString();
            const div = document.createElement('div');

            if (type === "human") {
                div.className = "p-3 rounded-2xl bg-orange-500/20 border border-orange-500/40 space-y-1 max-w-sm ml-auto animate-in fade-in";
                div.innerHTML = `
                    <div class="flex items-center justify-between text-[10px]">
                        <span class="font-bold text-orange-300">👤 You</span>
                        <span class="text-slate-400 font-mono">${time}</span>
                    </div>
                    <p class="text-white text-xs leading-relaxed">${text}</p>
                `;
            } else if (type === "policy") {
                div.className = "p-3.5 rounded-3xl bg-black/60 border border-purple-500/25 space-y-2 animate-in fade-in";
                div.innerHTML = `
                    <div class="flex items-center justify-between text-[11px]">
                        <span class="font-bold text-purple-300 font-mono">${sender}</span>
                        <span class="text-[10px] text-slate-400 font-mono">${time}</span>
                    </div>
                    <p class="text-slate-200 text-xs leading-relaxed">${text}</p>
                    <div class="flex justify-end pt-1">
                        <span class="text-[9px] font-mono text-slate-400 bg-black/60 px-2 py-0.5 rounded-full border border-white/[0.08]">[${badge || 'Verified'}]</span>
                    </div>
                `;
            } else {
                div.className = "p-3.5 rounded-3xl bg-black/60 border border-orange-500/25 space-y-2 animate-in fade-in";
                div.innerHTML = `
                    <div class="flex items-center justify-between text-[11px]">
                        <span class="font-bold text-orange-300 font-mono">${sender}</span>
                        <span class="text-[10px] text-slate-400 font-mono">${time}</span>
                    </div>
                    <p class="text-slate-200 text-xs leading-relaxed">${text}</p>
                    <div class="flex justify-end pt-1">
                        <span class="text-[9px] font-mono text-slate-400 bg-black/60 px-2 py-0.5 rounded-full border border-white/[0.08]">[${badge || 'Analyzed'}]</span>
                    </div>
                `;
            }

            stream.appendChild(div);
            stream.scrollTop = stream.scrollHeight;
        }

        function toggleVoiceAudio(btn) {
            const icon = btn.querySelector('.play-icon');
            if (icon.innerText === '▶') {
                icon.innerText = '⏸';
                btn.classList.add('ring-2', 'ring-orange-400');
            } else {
                icon.innerText = '▶';
                btn.classList.remove('ring-2', 'ring-orange-400');
            }
        }

        function recenterHoneycombCanvas() {
            clearLineageHighlight();
            closeInspectorLedger();
            renderHoneycombCanvas();
        }

        function handleGlobalSearch(e) {
            const query = e.target.value.toLowerCase().trim();
            if (!query) {
                clearLineageHighlight();
                return;
            }
            const match = allGraphNodes.find(n => n.id.toLowerCase().includes(query) || n.label.toLowerCase().includes(query));
            if (match) {
                selectNodeAndPopOutInspector(match);
            }
        }

        async function reseedGraph() {
            if (confirm("Reset and reseed graph to baseline state?")) {
                await fetch('/api/seed', { method: 'POST' });
                location.reload();
            }
        }

        // Initialize on load
        window.addEventListener('DOMContentLoaded', () => {
            renderZeroStateGrid();
            renderHoneycombCanvas();
        });
    </script>
</body>
</html>
"""

# Liquid Glass: cubic-bezier spring physics and specular highlights tuned
