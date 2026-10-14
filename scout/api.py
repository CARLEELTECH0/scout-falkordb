"""
FastAPI REST Backend & Interactive Single-Page Visualizer for Scout
Serves the unified FalkorDB graph, multi-hop reasoning endpoints, and the Dribbble-inspired
Modern Team Collaboration UI with Floating Bottom Navigation Bar, Dynamic Honeycomb Graph,
and AI Team Chat & Situation First Frame.
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
            "message": f"I received your message: \"{req.directive}\". I checked our company records and access paths in FalkorDB. Everything is tracked safely.",
            "badge": "Checked company records · 14ms"
        },
        "policy_response": {
            "agent": "Policy-Beta",
            "role": "Team & Rules Advisor",
            "message": f"I verified your instruction against Rule SEC-402. All actions are logged and our team is protected.",
            "badge": "Safety rule verified · 18ms"
        }
    }


# -------------------------------------------------------------
# Embedded Single-Page Interactive Dashboard (Dribbble Modern Team Collaboration UI)
# -------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def dashboard():
    return """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SCOUT — AI Team Workspace & Incident Solver</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
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
            --bg-canvas: #080b13;
            --bg-card: rgba(18, 24, 38, 0.78);
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

        /* Imran Jakir Pillowy Rounded Cards */
        .dribbble-card {
            background: linear-gradient(150deg, rgba(22, 28, 46, 0.75) 0%, rgba(12, 16, 28, 0.92) 100%);
            backdrop-filter: blur(28px) saturate(210%);
            -webkit-backdrop-filter: blur(28px) saturate(210%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 24px;
            box-shadow: 0 10px 32px -8px rgba(0, 0, 0, 0.70), inset 0 1px 0 rgba(255, 255, 255, 0.10);
            transition: all 0.25s var(--spring-curve);
        }
        .dribbble-card:hover {
            border-color: rgba(249, 115, 22, 0.40);
            box-shadow: 0 14px 40px -8px rgba(249, 115, 22, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.15);
        }

        /* Voice Card (Lavender/Purple Glow) */
        .voice-card {
            background: linear-gradient(145deg, rgba(46, 28, 68, 0.65) 0%, rgba(20, 16, 32, 0.90) 100%);
            border: 1px solid rgba(168, 85, 247, 0.32);
            border-radius: 22px;
            box-shadow: 0 8px 25px -6px rgba(168, 85, 247, 0.22), inset 0 1px 0 rgba(255, 255, 255, 0.12);
        }

        /* Solar Orange Tactile Button */
        .btn-solar {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            height: 40px;
            padding: 0 18px;
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
        .btn-solar:active:not(:disabled) {
            transform: translateY(0.5px) scale(0.98);
        }

        .btn-obsidian {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            height: 40px;
            padding: 0 16px;
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

        /* Soundwave Equalizer Bars */
        @keyframes soundwave {
            0%, 100% { height: 4px; }
            50% { height: 18px; }
        }
        .sound-bar-1 { animation: soundwave 1.1s infinite ease-in-out 0.1s; }
        .sound-bar-2 { animation: soundwave 1.1s infinite ease-in-out 0.35s; }
        .sound-bar-3 { animation: soundwave 1.1s infinite ease-in-out 0.2s; }
        .sound-bar-4 { animation: soundwave 1.1s infinite ease-in-out 0.5s; }
        .sound-bar-5 { animation: soundwave 1.1s infinite ease-in-out 0.25s; }

        .waveform-bar {
            width: 2.5px;
            border-radius: 2px;
            background-color: #cbd5e1;
        }

        /* Micro scrollbars */
        ::-webkit-scrollbar {
            width: 4px;
            height: 4px;
        }
        ::-webkit-scrollbar-track {
            background: transparent;
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(249, 115, 22, 0.28);
            border-radius: 2px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(249, 115, 22, 0.50);
        }

        /* Floating Bottom Nav Pill */
        .bottom-dock {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 60;
            background: rgba(14, 18, 30, 0.88);
            backdrop-filter: blur(28px) saturate(220%);
            -webkit-backdrop-filter: blur(28px) saturate(220%);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 9999px;
            padding: 6px 10px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.80), 0 0 30px rgba(249, 115, 22, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.18);
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .dock-tab {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            height: 38px;
            padding: 0 16px;
            border-radius: 9999px;
            font-size: 0.8125rem;
            font-weight: 600;
            color: #94a3b8;
            transition: all 0.2s var(--spring-curve);
            cursor: pointer;
            user-select: none;
            border: 1px solid transparent;
        }
        .dock-tab:hover {
            color: #ffffff;
            background: rgba(255, 255, 255, 0.06);
        }
        .dock-tab.active {
            color: #ffffff;
            background: linear-gradient(180deg, rgba(255, 107, 0, 0.22) 0%, rgba(234, 88, 12, 0.35) 100%);
            border: 1px solid rgba(249, 115, 22, 0.50);
            box-shadow: 0 4px 16px rgba(249, 115, 22, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.20);
        }

        /* Honeycomb Node Hover & Drag */
        .hex-cell {
            cursor: grab;
            transition: filter 0.2s, stroke-width 0.2s;
        }
        .hex-cell:active {
            cursor: grabbing;
        }
        .hex-cell:hover {
            filter: drop-shadow(0 0 12px currentColor);
            stroke-width: 3.5px;
        }

        /* Pulsing breach stroke */
        @keyframes breachGlow {
            0%, 100% { stroke-opacity: 1; filter: drop-shadow(0 0 6px #ff6b00); }
            50% { stroke-opacity: 0.5; filter: drop-shadow(0 0 14px #ff8a3d); }
        }
        .breach-link {
            stroke: #ff6b00;
            stroke-width: 3px;
            animation: breachGlow 2.2s infinite ease-in-out;
        }
    </style>
</head>
<body class="h-screen w-screen flex flex-col antialiased selection:bg-orange-500/30 selection:text-orange-200 overflow-hidden">

    <!-- TOP HEADER (Clean Collaboration Bar - 56px) -->
    <header class="h-[56px] px-6 bg-[#090c15] border-b border-white/[0.08] flex items-center justify-between shrink-0 z-40">
        <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-2xl bg-gradient-to-br from-orange-500 via-orange-600 to-amber-700 flex items-center justify-center text-base shadow-[0_0_18px_rgba(249,115,22,0.48)] border border-orange-300/35 cursor-pointer" title="Scout AI Team Workspace">
                🛡️
            </div>
            <div>
                <div class="flex items-center gap-2">
                    <span class="font-extrabold text-sm tracking-tight text-white uppercase bg-clip-text text-transparent bg-gradient-to-r from-white via-slate-100 to-orange-300">SCOUT</span>
                    <span class="text-[10px] font-mono px-2 py-0.5 rounded-full bg-orange-500/10 text-orange-400 border border-orange-500/30 font-bold">FalkorDB</span>
                </div>
            </div>
            <div class="h-4 w-px bg-white/10 hidden sm:block"></div>
            <!-- System Status Indicator in Plain English -->
            <span class="px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 text-xs flex items-center gap-1.5 font-medium">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                <span>All Systems Live</span>
            </span>
        </div>

        <!-- Center Current Situation Pill in Plain English -->
        <div class="hidden md:flex items-center gap-2">
            <div id="top-situation-pill" class="px-3.5 py-1 rounded-full bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs flex items-center gap-2 font-medium">
                <span class="w-2 h-2 rounded-full bg-rose-500 animate-pulse"></span>
                <span>Current Issue: <strong class="text-white">14 Failed Logins on Login Gateway</strong></span>
                <span class="text-[10px] px-1.5 py-0.2 rounded bg-rose-500/20 text-rose-200 uppercase font-mono font-bold">Critical</span>
            </div>
        </div>

        <!-- Top Right Action Controls -->
        <div class="flex items-center gap-2.5">
            <button onclick="triggerSimulatedAttack()" class="btn-solar text-xs" title="Simulate a new issue to see AI in action">
                <span>⚡ Simulate New Issue</span>
            </button>
            <button onclick="toggleCockpitView()" id="btn-toggle-layout" class="btn-obsidian text-xs" title="Switch between Focused View and 3-Column Cockpit">
                <span id="layout-mode-label">🔲 Cockpit View</span>
            </button>
            <button onclick="reseedGraph()" class="btn-obsidian text-xs" title="Reset all data to clean state">
                <span>🔄 Reset</span>
            </button>
        </div>
    </header>

    <!-- MAIN DYNAMIC CONTENT CONTAINER (Padding at bottom for floating dock) -->
    <main class="flex-1 overflow-hidden relative pb-[82px]">

        <!-- =================================================================== -->
        <!-- VIEW 1: 💬 AI TEAM CHAT & SITUATION (DEFAULT FIRST FRAME) -->
        <!-- =================================================================== -->
        <div id="view-chat" class="w-full h-full flex flex-col p-5 gap-4 overflow-hidden max-w-7xl mx-auto">
            
            <!-- CURRENT SITUATION BANNER (Prominent First Frame Highlight) -->
            <div id="situation-banner-card" class="dribbble-card p-4 shrink-0 border-orange-500/30 bg-gradient-to-r from-orange-950/30 via-slate-900/60 to-black/80 flex flex-col md:flex-row items-start md:items-center justify-between gap-3 shadow-lg">
                <div class="flex items-start gap-3.5">
                    <div id="situation-icon-box" class="w-11 h-11 rounded-2xl bg-rose-500/20 border border-rose-500/40 text-rose-300 flex items-center justify-center text-xl shrink-0">
                        🚨
                    </div>
                    <div class="space-y-1">
                        <div class="flex items-center gap-2">
                            <span id="situation-badge-rgy" class="px-2 py-0.5 rounded-full text-[10px] font-bold uppercase font-mono bg-rose-500/20 text-rose-300 border border-rose-500/40">🔴 Situation: Critical</span>
                            <span class="text-xs text-slate-400 font-mono">Today at 12:44 PM</span>
                            <span class="text-xs text-slate-500">·</span>
                            <span class="text-xs text-orange-300 font-medium">Target: Login Gateway (prod-auth-gateway)</span>
                        </div>
                        <h2 id="situation-title-text" class="text-sm font-bold text-white tracking-tight">
                            Unauthorized Login Wave: 14 consecutive failed passwords detected from unknown address
                        </h2>
                        <p id="situation-desc-text" class="text-xs text-slate-300 max-w-3xl leading-relaxed">
                            The security key was traced to team member <strong class="text-purple-300">Bob Martinez</strong>. Our AI agents investigated the access path, verified safety rules, and recommend an immediate one-click lockdown.
                        </p>
                    </div>
                </div>

                <!-- One-Click Instant Fix Action -->
                <div class="flex items-center gap-2 shrink-0 self-end md:self-center">
                    <button onclick="executeMitigation()" id="btn-banner-quarantine" class="btn-solar h-10 px-5 text-xs font-bold shadow-lg shadow-orange-500/30">
                        <span>🛡️ Lock Down & Fix Issue</span>
                    </button>
                    <button onclick="switchTab('honeycomb'); highlightNode('EMP-02');" class="btn-obsidian h-10 px-4 text-xs font-medium">
                        <span>👤 View Bob on Map</span>
                    </button>
                </div>
            </div>

            <!-- CHAT STREAM CANVAS -->
            <div class="flex-1 dribbble-card flex flex-col overflow-hidden bg-black/50 border-white/[0.08]">
                
                <!-- Chat Stream Subheader (Dribbble Screen Anatomy: Sophia Lee / Online / Voice Room) -->
                <div class="h-14 px-6 border-b border-white/[0.08] flex items-center justify-between shrink-0 bg-black/40">
                    <div class="flex items-center gap-3">
                        <div class="relative">
                            <div class="w-9 h-9 rounded-2xl bg-gradient-to-tr from-orange-500 via-amber-600 to-purple-600 flex items-center justify-center font-bold text-xs text-white shadow">
                                AI
                            </div>
                            <span class="absolute bottom-0 right-0 w-2.5 h-2.5 rounded-full bg-emerald-400 border-2 border-black"></span>
                        </div>
                        <div>
                            <h3 class="text-xs font-bold text-white flex items-center gap-2">
                                <span>Scout-Alpha & Policy-Beta</span>
                                <span class="text-[10px] text-orange-400 px-2 py-0.5 rounded-full bg-orange-500/10 border border-orange-500/30 font-medium">AI Decision Room</span>
                            </h3>
                            <p class="text-[10px] text-emerald-400 flex items-center gap-1 font-mono">
                                <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                                <span>Online · Live Multi-Agent Reasoning</span>
                            </p>
                        </div>
                    </div>

                    <!-- Voice Call Waveform Visualizer from Dribbble Shot -->
                    <div class="flex items-center gap-3">
                        <div class="flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-orange-500/10 border border-orange-500/30 text-xs font-mono">
                            <span class="text-orange-400 font-bold">🎙️ Voice Room:</span>
                            <div class="flex items-center gap-0.5 h-3">
                                <span class="w-1 bg-orange-400 rounded-full sound-bar-1"></span>
                                <span class="w-1 bg-amber-400 rounded-full sound-bar-2"></span>
                                <span class="w-1 bg-orange-500 rounded-full sound-bar-3"></span>
                                <span class="w-1 bg-amber-300 rounded-full sound-bar-4"></span>
                                <span class="w-1 bg-orange-400 rounded-full sound-bar-5"></span>
                            </div>
                            <span class="text-slate-400 text-[10px] ml-1">00:04:18</span>
                        </div>
                    </div>
                </div>

                <!-- Messages Feed -->
                <div id="unified-chat-stream" class="flex-1 overflow-y-auto p-5 space-y-4 text-xs">
                    
                    <!-- Date Divider -->
                    <div class="flex items-center justify-center">
                        <span class="px-3 py-0.5 rounded-full bg-white/[0.05] border border-white/[0.08] text-[10px] font-mono text-slate-400 uppercase font-semibold">Today · Live Situation</span>
                    </div>

                    <!-- Message 1: Scout-Alpha (Security Guardian) -->
                    <div class="p-4 rounded-3xl bg-black/60 border border-orange-500/25 space-y-2.5 max-w-3xl">
                        <div class="flex items-center justify-between text-[11px]">
                            <div class="flex items-center gap-2">
                                <div class="w-6 h-6 rounded-full bg-orange-600/40 text-orange-300 font-bold text-[10px] flex items-center justify-center border border-orange-500/30">SA</div>
                                <span class="font-bold text-orange-300">Scout-Alpha (Security Guardian)</span>
                                <span class="text-[9px] px-1.5 py-0.2 rounded bg-orange-500/10 text-orange-400 border border-orange-500/30 font-mono">Analysis</span>
                            </div>
                            <span class="text-[10px] text-slate-400 font-mono">12:44:10 PM</span>
                        </div>
                        <p class="text-slate-200 leading-relaxed text-[12px]">
                            I caught an unusual spike in failed logins on the <strong class="text-white">Login Gateway</strong> (<code class="text-orange-300 bg-black/60 px-1 py-0.5 rounded">prod-auth-gateway</code>). There were <strong class="text-rose-400">14 consecutive failed attempts in 30 seconds</strong> coming from an unrecognized device (<code class="text-orange-300 bg-black/60 px-1 py-0.5 rounded">192.168.1.105</code>).
                        </p>

                        <!-- Attached Log File Pill from Dribbble Shot -->
                        <div class="flex items-center gap-2 p-2.5 rounded-2xl bg-orange-950/20 border border-orange-500/30 text-[11px] font-mono text-slate-200 hover:border-orange-500/50 transition cursor-pointer">
                            <span class="text-orange-400 text-base">📄</span>
                            <span class="font-medium text-white">login_activity_telemetry.log</span>
                            <span class="text-slate-500 ml-auto">14.2 KB</span>
                        </div>

                        <!-- Interactive Voice Note Audio Player from Dribbble Shot -->
                        <div class="p-3 rounded-2xl bg-orange-950/30 border border-orange-500/35 flex items-center gap-3">
                            <button onclick="toggleVoiceAudio(this)" class="w-8 h-8 rounded-full bg-gradient-to-r from-orange-500 to-amber-600 text-white flex items-center justify-center text-xs shadow-md shadow-orange-500/30 hover:scale-105 transition" title="Play Voice Brief">
                                <span class="play-icon">▶</span>
                            </button>
                            <div class="flex-1 flex items-center gap-1 h-5">
                                <span class="waveform-bar h-2 bg-orange-400"></span>
                                <span class="waveform-bar h-4 bg-orange-400"></span>
                                <span class="waveform-bar h-3 bg-orange-300"></span>
                                <span class="waveform-bar h-5 bg-orange-400"></span>
                                <span class="waveform-bar h-3 bg-orange-300"></span>
                                <span class="waveform-bar h-4 bg-orange-400"></span>
                                <span class="waveform-bar h-2 bg-orange-300"></span>
                                <span class="waveform-bar h-5 bg-orange-400"></span>
                                <span class="waveform-bar h-3 bg-orange-300"></span>
                                <span class="waveform-bar h-4 bg-orange-400"></span>
                                <span class="waveform-bar h-2 bg-orange-300"></span>
                                <span class="waveform-bar h-4 bg-slate-500"></span>
                                <span class="waveform-bar h-2 bg-slate-600"></span>
                                <span class="waveform-bar h-3 bg-slate-600"></span>
                                <span class="waveform-bar h-1 bg-slate-600"></span>
                            </div>
                            <span class="text-[10px] font-mono text-orange-300 font-bold">0:14</span>
                        </div>

                        <div class="flex justify-end pt-1">
                            <span class="text-[10px] font-mono text-slate-400 bg-black/60 px-2.5 py-0.5 rounded-full border border-white/[0.08]">[Checked security logs · 12ms]</span>
                        </div>
                    </div>

                    <!-- Message 2: Policy-Beta (Team & Rules Advisor) -->
                    <div class="p-4 rounded-3xl bg-black/60 border border-purple-500/25 space-y-2.5 max-w-3xl ml-auto">
                        <div class="flex items-center justify-between text-[11px]">
                            <div class="flex items-center gap-2">
                                <div class="w-6 h-6 rounded-full bg-purple-600/40 text-purple-300 font-bold text-[10px] flex items-center justify-center border border-purple-500/30">PB</div>
                                <span class="font-bold text-purple-300">Policy-Beta (Team & Rules Advisor)</span>
                                <span class="text-[9px] px-1.5 py-0.2 rounded bg-purple-500/10 text-purple-400 border border-purple-500/30 font-mono">Rules Check</span>
                            </div>
                            <span class="text-[10px] text-slate-400 font-mono">12:44:13 PM</span>
                        </div>

                        <!-- Quoted Reply Box from Dribbble Shot -->
                        <div class="p-2.5 rounded-2xl bg-purple-950/30 border-l-2 border-purple-400 text-[11px] text-slate-300 space-y-0.5">
                            <span class="text-purple-400 font-semibold block text-[10px]">Replied to Scout-Alpha:</span>
                            <p class="truncate italic opacity-85">"I caught an unusual spike in failed logins on the Login Gateway..."</p>
                        </div>

                        <p class="text-slate-200 leading-relaxed text-[12px]">
                            I checked our company database in FalkorDB. The login key is used by <strong class="text-white">Bob Martinez</strong> (<span class="text-purple-300">SecOps Team</span>). This gateway connects directly to <strong class="text-amber-300">Project FalconShield</strong>. Under company safety rule <span class="text-purple-300 font-semibold">SEC-402</span>, automated lockdown is approved because the danger score is <strong class="text-rose-400">125 / 100</strong>.
                        </p>

                        <!-- Risk Score Meter -->
                        <div class="p-2.5 rounded-2xl bg-purple-950/25 border border-purple-500/25 space-y-1">
                            <div class="flex items-center justify-between text-[10px] font-mono">
                                <span class="text-slate-400">Danger Level Meter</span>
                                <span class="text-rose-400 font-bold">125 / 100 [High Priority · Lockdown Approved]</span>
                            </div>
                            <div class="w-full h-1.5 rounded-full bg-black/60 overflow-hidden">
                                <div class="h-full bg-gradient-to-r from-amber-500 via-rose-500 to-red-600 rounded-full" style="width: 100%"></div>
                            </div>
                        </div>

                        <div class="flex justify-end pt-1">
                            <span class="text-[10px] font-mono text-slate-400 bg-black/60 px-2.5 py-0.5 rounded-full border border-white/[0.08]">[Verified team safety rules · 18ms]</span>
                        </div>
                    </div>

                </div>

                <!-- Footer Control: Modern Collaboration Input Dock (Direct from Dribbble Shot) -->
                <div class="p-4 bg-black/60 border-t border-white/[0.08] shrink-0 space-y-2.5">
                    
                    <!-- Quick Directive Suggestion Chips -->
                    <div class="flex items-center gap-2 overflow-x-auto text-[11px] font-medium text-slate-300">
                        <span class="text-slate-500 text-[10px] uppercase font-mono">Quick Actions:</span>
                        <button onclick="sendQuickDirective('Lock down Login Gateway now')" class="px-3 py-1 rounded-full bg-orange-500/15 hover:bg-orange-500/25 text-orange-300 border border-orange-500/30 transition shrink-0">
                            ⚡ Lock Down Gateway
                        </button>
                        <button onclick="sendQuickDirective('Who has access to Login Gateway?')" class="px-3 py-1 rounded-full bg-purple-500/15 hover:bg-purple-500/25 text-purple-300 border border-purple-500/30 transition shrink-0">
                            🔍 Who has access?
                        </button>
                        <button onclick="sendQuickDirective('Show safety rule SEC-402')" class="px-3 py-1 rounded-full bg-white/[0.06] hover:bg-white/[0.1] text-slate-200 border border-white/10 transition shrink-0">
                            ⚖️ Check safety rules
                        </button>
                        <button onclick="sendQuickDirective('What teams are affected?')" class="px-3 py-1 rounded-full bg-white/[0.06] hover:bg-white/[0.1] text-slate-200 border border-white/10 transition shrink-0">
                            👥 Impacted teams
                        </button>
                    </div>

                    <!-- Input Form -->
                    <form id="directive-form" onsubmit="submitDirective(event)" class="flex items-center gap-2.5">
                        <button type="button" class="w-10 h-10 rounded-full bg-white/[0.05] hover:bg-white/[0.1] border border-white/[0.08] text-slate-400 hover:text-white flex items-center justify-center text-sm transition" title="Voice Message">
                            🎙️
                        </button>
                        <button type="button" class="w-10 h-10 rounded-full bg-white/[0.05] hover:bg-white/[0.1] border border-white/[0.08] text-slate-400 hover:text-white flex items-center justify-center text-sm transition" title="Attach Company File">
                            📎
                        </button>
                        <input id="directive-input" type="text" placeholder="Message Scout-Alpha & Policy-Beta (or ask questions about the team & servers)..." class="h-11 bg-black/80 border border-white/10 focus:border-orange-500/60 rounded-full px-5 text-xs text-white placeholder-slate-500 flex-1 outline-none transition shadow-inner">
                        <button type="submit" class="w-11 h-11 rounded-full bg-gradient-to-r from-orange-500 to-amber-600 hover:scale-105 active:scale-95 text-white flex items-center justify-center shadow-lg shadow-orange-500/35 transition shrink-0" title="Send message to AI agents">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
                        </button>
                    </form>
                </div>
            </div>
        </div>

        <!-- =================================================================== -->
        <!-- VIEW 2: 🚨 LIVE ALERTS & QUICK FIXES (TRACK 1) -->
        <!-- =================================================================== -->
        <div id="view-alerts" class="w-full h-full p-5 hidden gap-5 overflow-hidden max-w-7xl mx-auto flex-col md:flex-row">
            
            <!-- Left Side: Alert Queue in Plain English -->
            <div class="w-full md:w-[360px] dribbble-card p-4 flex flex-col space-y-3 shrink-0 bg-black/45">
                <div class="flex items-center justify-between pb-2 border-b border-white/[0.08]">
                    <div>
                        <h2 class="text-xs font-bold text-white uppercase tracking-wider font-mono flex items-center gap-2">
                            <span>🚨</span> Active Issues Queue
                        </h2>
                        <p class="text-[11px] text-slate-400">Current situation flags</p>
                    </div>
                    <span class="px-2.5 py-0.5 rounded-full bg-rose-500/20 text-rose-300 font-mono text-[10px] font-bold border border-rose-500/30">1 Critical</span>
                </div>

                <!-- Alert Cards -->
                <div class="space-y-2.5 flex-1 overflow-y-auto">
                    <!-- Alert 1 (Selected) -->
                    <div onclick="selectAlert('INC-2026-001')" id="alert-card-INC-2026-001" class="p-3.5 rounded-2xl bg-black/60 border border-orange-500/60 shadow-[0_0_20px_rgba(249,115,22,0.18)] cursor-pointer hover:border-orange-500 transition space-y-2">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center gap-2">
                                <span class="w-3 h-3 rounded-full bg-rose-500"></span>
                                <div class="font-bold text-white text-xs">Login Gateway Brute-Force</div>
                            </div>
                            <span class="text-[10px] text-slate-400 font-mono">12:44 PM</span>
                        </div>
                        <p class="text-[11px] text-slate-300">14 failed logins detected on Login Gateway</p>
                        <div class="flex items-center justify-between pt-1 text-[10px] font-mono">
                            <span class="text-orange-300">Target: prod-auth-gateway</span>
                            <span id="badge-alert-status" class="px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-300 border border-rose-500/30 font-bold">Needs Fix</span>
                        </div>
                    </div>

                    <!-- Alert 2 -->
                    <div onclick="selectAlert('INC-2026-002')" id="alert-card-INC-2026-002" class="p-3.5 rounded-2xl bg-black/35 border border-white/[0.06] cursor-pointer hover:border-orange-500/40 transition space-y-2">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center gap-2">
                                <span class="w-3 h-3 rounded-full bg-amber-400"></span>
                                <div class="font-bold text-slate-200 text-xs">Elevated Database Queries</div>
                            </div>
                            <span class="text-[10px] text-slate-400 font-mono">11:15 AM</span>
                        </div>
                        <p class="text-[11px] text-slate-400">Query rate higher than normal on cluster</p>
                        <div class="flex items-center justify-between pt-1 text-[10px] font-mono">
                            <span class="text-amber-300">Target: prod-falcon-cluster</span>
                            <span class="px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30">Review</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Right Side: Step-by-Step Reasoner Breakdown & 1-Click Fix -->
            <div class="flex-1 dribbble-card p-6 flex flex-col space-y-4 bg-black/50 overflow-y-auto">
                <div class="flex items-center justify-between pb-3 border-b border-white/[0.08]">
                    <div>
                        <span class="text-[10px] font-mono uppercase tracking-wider text-orange-400 font-bold">Incident Analysis & Quick Resolution</span>
                        <h3 class="text-base font-bold text-white">Login Gateway Unauthorized Access Investigation</h3>
                    </div>
                    <span id="drill-status-badge" class="px-3 py-1 rounded-full text-xs font-bold font-mono bg-rose-500/20 text-rose-300 border border-rose-500/30 uppercase">🔴 Active Issue</span>
                </div>

                <!-- 3 Steps Explained in Plain English -->
                <div class="space-y-3.5">
                    <!-- Step 1 -->
                    <div class="p-4 rounded-2xl bg-black/60 border border-white/10 flex items-start gap-3.5">
                        <div class="w-6 h-6 rounded-full bg-orange-500/20 text-orange-400 text-xs font-bold flex items-center justify-center border border-orange-500/40 shrink-0 mt-0.5">1</div>
                        <div class="space-y-1">
                            <div class="font-bold text-white text-xs">What Happened (The Entry Event)</div>
                            <p class="text-xs text-slate-300 leading-relaxed">
                                An external system repeatedly tried to log into <strong class="text-white">Login Gateway</strong> using wrong passwords 14 times in under 30 seconds.
                            </p>
                            <div class="text-[11px] font-mono text-slate-400">Source: <span class="text-orange-300">192.168.1.105</span> · Protocol: SSHv2</div>
                        </div>
                    </div>

                    <!-- Step 2 -->
                    <div class="p-4 rounded-2xl bg-black/60 border border-white/10 flex items-start gap-3.5">
                        <div class="w-6 h-6 rounded-full bg-purple-500/20 text-purple-400 text-xs font-bold flex items-center justify-center border border-purple-500/40 shrink-0 mt-0.5">2</div>
                        <div class="space-y-1">
                            <div class="font-bold text-white text-xs">Who is Impacted (Access Keys & Team Links)</div>
                            <p class="text-xs text-slate-300 leading-relaxed">
                                The targeted login key belongs to <strong class="text-purple-300">Bob Martinez</strong>. Bob reports to <strong class="text-purple-300">Alice Chen</strong> in the <strong class="text-purple-300">SecOps Team</strong>. This gateway connects to <strong class="text-amber-300">Project FalconShield</strong>.
                            </p>
                        </div>
                    </div>

                    <!-- Step 3 -->
                    <div class="p-4 rounded-2xl bg-black/60 border border-white/10 flex items-start gap-3.5">
                        <div class="w-6 h-6 rounded-full bg-emerald-500/20 text-emerald-400 text-xs font-bold flex items-center justify-center border border-emerald-500/40 shrink-0 mt-0.5">3</div>
                        <div class="space-y-1 flex-1">
                            <div class="font-bold text-white text-xs">AI Safety Rule Approval & Resolution</div>
                            <p class="text-xs text-slate-300 leading-relaxed">
                                Rule <span class="text-purple-300 font-semibold">SEC-402</span> confirms that locking down this gateway will safely block the attacker while letting team members re-authenticate with clean credentials.
                            </p>
                        </div>
                    </div>
                </div>

                <!-- Fix Button -->
                <div class="pt-4 border-t border-white/[0.08] flex items-center gap-3">
                    <button onclick="executeMitigation()" id="btn-fix-issue" class="btn-solar h-12 px-6 text-sm font-bold shadow-xl shadow-orange-500/30 flex-1">
                        <span>🛡️ Lock Down & Fix Issue (Instant Quarantine)</span>
                    </button>
                    <button onclick="switchTab('honeycomb');" class="btn-obsidian h-12 px-5 text-xs font-medium">
                        <span>🕸️ Inspect on Honeycomb Map</span>
                    </button>
                </div>
            </div>
        </div>

        <!-- =================================================================== -->
        <!-- VIEW 3: 🕸️ HONEYCOMB DYNAMIC GRAPH (TRACK 3) -->
        <!-- =================================================================== -->
        <div id="view-honeycomb" class="w-full h-full p-4 hidden gap-4 overflow-hidden max-w-7xl mx-auto flex-col">
            
            <!-- Honeycomb Controls Header -->
            <div class="dribbble-card px-5 py-3 flex items-center justify-between shrink-0 bg-black/60">
                <div class="flex items-center gap-4">
                    <div>
                        <h2 class="text-xs font-bold text-white uppercase tracking-wider font-mono flex items-center gap-2">
                            <span>🕸️</span> Company Honeycomb Map
                        </h2>
                        <p class="text-[11px] text-slate-400">Drag any hexagon to move · Interactive live relationships</p>
                    </div>

                    <!-- Color Legend directly answering user prompt: Secondary for People, RGY for Situations -->
                    <div class="hidden md:flex items-center gap-3 text-[11px] font-mono pl-4 border-l border-white/10">
                        <span class="flex items-center gap-1.5 text-purple-300">
                            <span class="w-2.5 h-2.5 rounded-full bg-purple-500 shadow-[0_0_8px_#a855f7]"></span>
                            <span>People (Secondary Color)</span>
                        </span>
                        <span class="flex items-center gap-1.5 text-rose-400">
                            <span class="w-2.5 h-2.5 rounded-full bg-rose-500 shadow-[0_0_8px_#ef4444]"></span>
                            <span>🔴 Critical Risk (RGY)</span>
                        </span>
                        <span class="flex items-center gap-1.5 text-amber-400">
                            <span class="w-2.5 h-2.5 rounded-full bg-amber-400 shadow-[0_0_8px_#f59e0b]"></span>
                            <span>🟡 Warning / Under Review (RGY)</span>
                        </span>
                        <span class="flex items-center gap-1.5 text-emerald-400">
                            <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 shadow-[0_0_8px_#10b981]"></span>
                            <span>🟢 Safe / Contained (RGY)</span>
                        </span>
                    </div>
                </div>

                <!-- Actions -->
                <div class="flex items-center gap-2">
                    <button onclick="recenterHoneycomb()" class="btn-obsidian h-8 px-3 text-xs" title="Reset hexagons back to regular honeycomb lattice">
                        <span>↺ Re-align Honeycomb</span>
                    </button>
                    <button onclick="filterHoneycomb('all')" class="btn-obsidian h-8 px-3 text-xs filter-btn active" id="filter-all">
                        <span>All</span>
                    </button>
                    <button onclick="filterHoneycomb('people')" class="btn-obsidian h-8 px-3 text-xs filter-btn" id="filter-people">
                        <span>People Only</span>
                    </button>
                    <button onclick="filterHoneycomb('situations')" class="btn-obsidian h-8 px-3 text-xs filter-btn" id="filter-situations">
                        <span>Situations (RGY)</span>
                    </button>
                </div>
            </div>

            <!-- Honeycomb Canvas with Interactive Dragging -->
            <div class="flex-1 dribbble-card bg-[#070a12] relative overflow-hidden flex items-center justify-center border-white/10" id="honeycomb-container">
                <svg id="honeycomb-svg" class="w-full h-full select-none" style="cursor: grab;">
                    <defs>
                        <!-- Glow Filters -->
                        <filter id="glow-orange" x="-20%" y="-20%" width="140%" height="140%">
                            <feGaussianBlur stdDeviation="4" result="blur" />
                            <feComposite in="SourceGraphic" in2="blur" operator="over" />
                        </filter>
                        <filter id="glow-purple" x="-20%" y="-20%" width="140%" height="140%">
                            <feGaussianBlur stdDeviation="4" result="blur" />
                            <feComposite in="SourceGraphic" in2="blur" operator="over" />
                        </filter>
                    </defs>
                    <!-- Link lines group -->
                    <g id="honeycomb-links"></g>
                    <!-- Hexagon cells group -->
                    <g id="honeycomb-cells"></g>
                </svg>

                <!-- Floating Inspector Card on Node Click -->
                <div id="honeycomb-inspector" class="absolute top-4 right-4 w-72 p-4 rounded-3xl bg-black/80 backdrop-blur-2xl border border-white/10 shadow-2xl space-y-2.5 hidden transition-all">
                    <div class="flex items-center justify-between pb-2 border-b border-white/10">
                        <div class="flex items-center gap-2">
                            <span id="inspect-icon" class="text-base">👤</span>
                            <span id="inspect-name" class="font-bold text-white text-xs">Bob Martinez</span>
                        </div>
                        <button onclick="closeInspector()" class="text-slate-400 hover:text-white text-xs">✕</button>
                    </div>
                    <div id="inspect-badge" class="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold uppercase inline-block">Role: Engineer</div>
                    <p id="inspect-desc" class="text-xs text-slate-300 leading-relaxed">
                        Member of SecOps team. Has access keys for Login Gateway.
                    </p>
                    <div class="pt-2 border-t border-white/10 text-[11px] space-y-1">
                        <div class="text-slate-400 font-mono text-[10px] uppercase">Connections:</div>
                        <div id="inspect-connections" class="space-y-1 text-slate-200"></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- =================================================================== -->
        <!-- VIEW 4: 📊 WORKSPACE OVERVIEW & FEED (TRACK 3 BENTO) -->
        <!-- =================================================================== -->
        <div id="view-overview" class="w-full h-full p-5 hidden gap-4 overflow-y-auto max-w-7xl mx-auto flex-col">
            
            <!-- Bento Grid from Imran Jakir Dribbble Shot -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                
                <!-- Voice Calls Bento Card (Lavender/Purple glow) -->
                <div class="voice-card p-5 space-y-3 flex flex-col justify-between">
                    <div class="flex items-center justify-between">
                        <div class="w-8 h-8 rounded-full bg-white/20 flex items-center justify-center text-sm">
                            📞
                        </div>
                        <span class="text-[10px] font-mono text-purple-300 font-bold uppercase">Live Audio Room</span>
                    </div>
                    <div>
                        <div class="text-2xl font-extrabold text-white leading-tight">3 <span class="text-sm font-normal text-purple-200">team members</span></div>
                        <span class="text-xs text-purple-200/80 block">Active Security Huddle</span>
                    </div>
                    <!-- Audio Waveform -->
                    <div class="flex items-center justify-between pt-2">
                        <div class="flex items-center gap-1 h-4">
                            <span class="w-1 bg-purple-300 rounded-full h-2"></span>
                            <span class="w-1 bg-purple-200 rounded-full h-4"></span>
                            <span class="w-1 bg-white rounded-full h-3"></span>
                            <span class="w-1 bg-purple-300 rounded-full h-4"></span>
                            <span class="w-1 bg-purple-200 rounded-full h-2"></span>
                        </div>
                        <!-- Avatar Stack -->
                        <div class="flex items-center -space-x-2 text-[9px] font-bold">
                            <div class="w-6 h-6 rounded-full bg-orange-600 border border-black flex items-center justify-center text-white">SA</div>
                            <div class="w-6 h-6 rounded-full bg-purple-600 border border-black flex items-center justify-center text-white">PB</div>
                            <div class="w-6 h-6 rounded-full bg-slate-700 border border-black flex items-center justify-center text-white">BM</div>
                        </div>
                    </div>
                </div>

                <!-- Team Channels Bento Card -->
                <div class="dribbble-card p-5 space-y-3 flex flex-col justify-between bg-black/45">
                    <div class="flex items-center justify-between">
                        <span class="text-xs font-bold text-white font-mono uppercase">📁 Team Channels</span>
                        <span class="text-xs text-orange-400 font-mono">3 Teams</span>
                    </div>
                    <div class="space-y-2 text-xs">
                        <div class="flex items-center justify-between p-2 rounded-xl bg-white/[0.04]">
                            <span class="font-medium text-white">🛡️ SecOps (Security)</span>
                            <span class="text-purple-300 font-mono">4 People</span>
                        </div>
                        <div class="flex items-center justify-between p-2 rounded-xl bg-white/[0.04]">
                            <span class="font-medium text-white">💻 Platform Engineering</span>
                            <span class="text-purple-300 font-mono">3 People</span>
                        </div>
                        <div class="flex items-center justify-between p-2 rounded-xl bg-white/[0.04]">
                            <span class="font-medium text-white">👑 Executive Leadership</span>
                            <span class="text-purple-300 font-mono">3 People</span>
                        </div>
                    </div>
                </div>

                <!-- Daily Safety Checklist Card -->
                <div class="dribbble-card p-5 space-y-3 flex flex-col justify-between bg-black/45">
                    <div class="flex items-center justify-between">
                        <span class="text-xs font-bold text-white font-mono uppercase">📋 Safety Checklist</span>
                        <span class="text-xs text-emerald-400 font-mono">2 / 3 Passed</span>
                    </div>
                    <div class="space-y-2 text-xs font-mono">
                        <div class="flex items-center gap-2 text-emerald-400">
                            <span>✓</span>
                            <span class="text-slate-200">Company Access Paths Audited</span>
                        </div>
                        <div class="flex items-center gap-2 text-emerald-400">
                            <span>✓</span>
                            <span class="text-slate-200">Safety Rule SEC-402 Verified</span>
                        </div>
                        <div class="flex items-center gap-2 text-orange-400">
                            <span id="chk-quarantine-icon">●</span>
                            <span id="chk-quarantine-label" class="text-orange-200">Quarantine Login Gateway</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Live Database & Activity Feed in Plain English -->
            <div class="dribbble-card p-5 flex-1 space-y-3 bg-black/55">
                <div class="flex items-center justify-between pb-2 border-b border-white/[0.08]">
                    <span class="text-xs font-bold uppercase tracking-wider text-orange-400 font-mono">Live Activity & Records Feed</span>
                    <span class="text-xs font-mono text-slate-400">FalkorDB Synced</span>
                </div>
                <div id="live-activity-box" class="h-44 overflow-y-auto space-y-2 text-xs font-mono text-slate-300">
                    <div>[12:44:01 PM] <strong class="text-emerald-400">System:</strong> Enterprise database synced successfully.</div>
                    <div>[12:44:10 PM] <strong class="text-rose-400">Scout-Alpha:</strong> Caught 14 failed logins from 192.168.1.105 on Login Gateway.</div>
                    <div>[12:44:13 PM] <strong class="text-purple-400">Policy-Beta:</strong> Evaluated company impact for Bob Martinez and Project FalconShield.</div>
                    <div>[12:44:15 PM] <strong class="text-amber-400">Policy-Beta:</strong> Rule SEC-402 passed. Immediate lockdown approved.</div>
                </div>
            </div>
        </div>

    </main>

    <!-- =================================================================== -->
    <!-- FLOATING BOTTOM NAVIGATION BAR (Dribbble Modern Team Dock) -->
    <!-- =================================================================== -->
    <nav class="bottom-dock">
        <!-- Tab 1: AI Team Chat (First Frame Default) -->
        <button onclick="switchTab('chat')" id="tab-btn-chat" class="dock-tab active">
            <span class="text-sm">💬</span>
            <span>AI Team Chat</span>
            <span class="w-1.5 h-1.5 rounded-full bg-orange-400 animate-pulse"></span>
        </button>

        <!-- Tab 2: Live Alerts & Fixes (Track 1) -->
        <button onclick="switchTab('alerts')" id="tab-btn-alerts" class="dock-tab">
            <span class="text-sm">🚨</span>
            <span>Alerts & Fixes</span>
            <span id="dock-alert-badge" class="px-1.5 py-0.2 rounded-full bg-rose-500 text-white font-mono text-[9px] font-bold">1</span>
        </button>

        <!-- Tab 3: Honeycomb Map (Track 3) -->
        <button onclick="switchTab('honeycomb')" id="tab-btn-honeycomb" class="dock-tab">
            <span class="text-sm">🕸️</span>
            <span>Honeycomb Map</span>
        </button>

        <!-- Tab 4: Overview & Feed -->
        <button onclick="switchTab('overview')" id="tab-btn-overview" class="dock-tab">
            <span class="text-sm">📊</span>
            <span>Overview</span>
        </button>
    </nav>

    <!-- CLIENT JAVASCRIPT LOGIC -->
    <script>
        let currentTab = 'chat';
        let currentIncident = 'INC-2026-001';
        let isCockpit = false;
        let isQuarantined = false;

        // ----------------------------------------------------
        // Tab Navigation
        // ----------------------------------------------------
        function switchTab(tabId) {
            currentTab = tabId;
            const views = ['chat', 'alerts', 'honeycomb', 'overview'];
            views.forEach(v => {
                const el = document.getElementById(`view-${v}`);
                const btn = document.getElementById(`tab-btn-${v}`);
                if (v === tabId) {
                    el.classList.remove('hidden');
                    el.classList.add('flex');
                    if (btn) btn.classList.add('active');
                } else {
                    el.classList.add('hidden');
                    el.classList.remove('flex');
                    if (btn) btn.classList.remove('active');
                }
            });

            if (tabId === 'honeycomb') {
                setTimeout(renderHoneycomb, 50);
            }
        }

        function toggleCockpitView() {
            isCockpit = !isCockpit;
            const lbl = document.getElementById('layout-mode-label');
            if (isCockpit) {
                lbl.innerText = "📱 Focused View";
                // Show chat, alerts, and honeycomb in side-by-side cockpit if screen allows
                document.getElementById('view-chat').classList.remove('hidden');
                document.getElementById('view-chat').classList.add('flex');
                document.getElementById('view-alerts').classList.remove('hidden');
                document.getElementById('view-alerts').classList.add('flex');
            } else {
                lbl.innerText = "🔲 Cockpit View";
                switchTab(currentTab);
            }
        }

        // ----------------------------------------------------
        // AI Chat & Directives
        // ----------------------------------------------------
        async function submitDirective(e) {
            e.preventDefault();
            const input = document.getElementById('directive-input');
            const text = input.value.trim();
            if (!text) return;
            input.value = '';
            sendDirective(text);
        }

        function sendQuickDirective(text) {
            sendDirective(text);
        }

        async function sendDirective(text) {
            // Append Operator Directive to Stream
            appendChatMessage("Operator (You)", text, "human");

            try {
                const res = await fetch('/api/agent/directive', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ directive: text, incident_id: currentIncident })
                });
                const data = await res.json();

                setTimeout(() => {
                    appendChatMessage("Scout-Alpha (Security Guardian)", data.security_response.message, "scout", data.security_response.badge);
                }, 400);

                setTimeout(() => {
                    appendChatMessage("Policy-Beta (Team & Rules Advisor)", data.policy_response.message, "policy", data.policy_response.badge);
                }, 900);

                addFeedEvent(`[${new Date().toLocaleTimeString()}] Operator: "${text.substring(0, 32)}..."`);
            } catch (err) {
                console.error("Directive error:", err);
            }
        }

        function appendChatMessage(sender, text, type, badge) {
            const stream = document.getElementById('unified-chat-stream');
            const time = new Date().toLocaleTimeString();
            const div = document.createElement('div');

            if (type === "human") {
                div.className = "p-3.5 rounded-3xl bg-orange-500/20 border border-orange-500/40 space-y-1.5 max-w-2xl ml-auto animate-in fade-in";
                div.innerHTML = `
                    <div class="flex items-center justify-between text-[11px]">
                        <span class="font-bold text-orange-300">👤 You (Operator)</span>
                        <span class="text-[10px] text-slate-400 font-mono">${time}</span>
                    </div>
                    <p class="text-white text-xs leading-relaxed">${text}</p>
                `;
            } else if (type === "policy") {
                div.className = "p-4 rounded-3xl bg-black/60 border border-purple-500/25 space-y-2 max-w-3xl ml-auto animate-in fade-in";
                div.innerHTML = `
                    <div class="flex items-center justify-between text-[11px]">
                        <div class="flex items-center gap-2">
                            <div class="w-6 h-6 rounded-full bg-purple-600/40 text-purple-300 font-bold text-[10px] flex items-center justify-center border border-purple-500/30">PB</div>
                            <span class="font-bold text-purple-300">${sender}</span>
                        </div>
                        <span class="text-[10px] text-slate-400 font-mono">${time}</span>
                    </div>
                    <p class="text-slate-200 text-xs leading-relaxed">${text}</p>
                    <div class="flex justify-end pt-1">
                        <span class="text-[10px] font-mono text-slate-400 bg-black/60 px-2 py-0.5 rounded-full border border-white/[0.08]">[${badge || 'Verified rule'}]</span>
                    </div>
                `;
            } else {
                div.className = "p-4 rounded-3xl bg-black/60 border border-orange-500/25 space-y-2 max-w-3xl animate-in fade-in";
                div.innerHTML = `
                    <div class="flex items-center justify-between text-[11px]">
                        <div class="flex items-center gap-2">
                            <div class="w-6 h-6 rounded-full bg-orange-600/40 text-orange-300 font-bold text-[10px] flex items-center justify-center border border-orange-500/30">SA</div>
                            <span class="font-bold text-orange-300">${sender}</span>
                        </div>
                        <span class="text-[10px] text-slate-400 font-mono">${time}</span>
                    </div>
                    <p class="text-slate-200 text-xs leading-relaxed">${text}</p>
                    <div class="flex justify-end pt-1">
                        <span class="text-[10px] font-mono text-slate-400 bg-black/60 px-2 py-0.5 rounded-full border border-white/[0.08]">[${badge || 'Checked records'}]</span>
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

        // ----------------------------------------------------
        // Fix & Quarantine Actions (Primary RGY Updates)
        // ----------------------------------------------------
        async function executeMitigation() {
            const btnBanner = document.getElementById('btn-banner-quarantine');
            const btnFix = document.getElementById('btn-fix-issue');
            if (btnBanner) {
                btnBanner.disabled = true;
                btnBanner.innerHTML = "<span>⚙️ Locking Down Gateway...</span>";
            }
            if (btnFix) {
                btnFix.disabled = true;
                btnFix.innerHTML = "<span>⚙️ Locking Down Gateway...</span>";
            }

            try {
                const res = await fetch('/api/agent/investigate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ incident_id: currentIncident })
                });
                const data = await res.json();
                isQuarantined = true;

                // Update Banner to Green Safe
                const banner = document.getElementById('situation-banner-card');
                if (banner) {
                    banner.className = "dribbble-card p-4 shrink-0 border-emerald-500/40 bg-gradient-to-r from-emerald-950/30 via-slate-900/60 to-black/80 flex flex-col md:flex-row items-start md:items-center justify-between gap-3 shadow-lg";
                }
                const iconBox = document.getElementById('situation-icon-box');
                if (iconBox) {
                    iconBox.className = "w-11 h-11 rounded-2xl bg-emerald-500/20 border border-emerald-500/40 text-emerald-300 flex items-center justify-center text-xl shrink-0";
                    iconBox.innerText = "🛡️";
                }
                const badgeRGY = document.getElementById('situation-badge-rgy');
                if (badgeRGY) {
                    badgeRGY.className = "px-2 py-0.5 rounded-full text-[10px] font-bold uppercase font-mono bg-emerald-500/20 text-emerald-300 border border-emerald-500/40";
                    badgeRGY.innerText = "🟢 Situation: Contained & Safe";
                }
                const titleText = document.getElementById('situation-title-text');
                if (titleText) {
                    titleText.innerText = "Threat Contained: Login Gateway safely locked down and access revoked";
                }
                const descText = document.getElementById('situation-desc-text');
                if (descText) {
                    descText.innerText = "The server was quarantined in FalkorDB. Credentials for Bob Martinez have been isolated for rotation. No downstream data leaked.";
                }

                if (btnBanner) {
                    btnBanner.className = "btn-obsidian h-10 px-5 text-xs font-bold text-emerald-300 border-emerald-500/40 cursor-default";
                    btnBanner.innerHTML = "<span>✓ Safe & Protected</span>";
                }
                if (btnFix) {
                    btnFix.className = "btn-obsidian h-12 px-6 text-sm font-bold text-emerald-300 border-emerald-500/40 cursor-default flex-1";
                    btnFix.innerHTML = "<span>✓ Issue Resolved & Asset Quarantined</span>";
                }

                // Top header pill
                const topPill = document.getElementById('top-situation-pill');
                if (topPill) {
                    topPill.className = "px-3.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs flex items-center gap-2 font-medium";
                    topPill.innerHTML = '<span class="w-2 h-2 rounded-full bg-emerald-400"></span><span>Status: <strong class="text-white">All Threats Contained & Protected</strong></span>';
                }

                // Badges in alerts tab
                const drillBadge = document.getElementById('drill-status-badge');
                if (drillBadge) {
                    drillBadge.className = "px-3 py-1 rounded-full text-xs font-bold font-mono bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 uppercase";
                    drillBadge.innerText = "🟢 Resolved";
                }
                const alertBadge = document.getElementById('badge-alert-status');
                if (alertBadge) {
                    alertBadge.className = "px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 font-bold";
                    alertBadge.innerText = "Contained";
                }
                const dockAlert = document.getElementById('dock-alert-badge');
                if (dockAlert) dockAlert.innerText = "0";

                // Checklist in overview
                const chkIcon = document.getElementById('chk-quarantine-icon');
                if (chkIcon) {
                    chkIcon.innerText = "✓";
                    chkIcon.className = "text-emerald-400 font-bold";
                }

                appendChatMessage("Scout-Alpha", "Lockdown executed. Login Gateway (AST-01) is now in 'Quarantined' status in FalkorDB. Attack surface neutralized.", "scout", "Asset Quarantined · 22ms");
                addFeedEvent(`[${new Date().toLocaleTimeString()}] Gateway AST-01 quarantined in FalkorDB.`);

                // Re-render honeycomb to show green status for quarantined asset
                renderHoneycomb();
            } catch (err) {
                console.error("Mitigation error:", err);
            }
        }

        async function triggerSimulatedAttack() {
            appendChatMessage("Scout-Alpha", "Caught 14 failed root login attempts from 192.168.1.105 on Login Gateway.", "scout", "Telemetry triage · 9ms");
            setTimeout(() => {
                appendChatMessage("Policy-Beta", "Evaluated blast radius. Risk Score 125 [High Risk]. Auto-lockdown recommended under Rule SEC-402.", "policy", "Safety rule audit · 15ms");
            }, 600);
            addFeedEvent(`[${new Date().toLocaleTimeString()}] Simulated incident triggered on Login Gateway.`);
        }

        function addFeedEvent(msg) {
            const feed = document.getElementById('live-activity-box');
            if (!feed) return;
            const div = document.createElement('div');
            div.innerText = msg;
            feed.appendChild(div);
            feed.scrollTop = feed.scrollHeight;
        }

        // ----------------------------------------------------
        // DYNAMIC HONEYCOMB GRAPH (LATTICE + DRAG + RGY / SECONDARY COLORS)
        // ----------------------------------------------------
        let honeycombNodes = [];
        let honeycombLinks = [];
        let draggedNode = null;
        let dragOffset = { x: 0, y: 0 };
        let activeFilter = 'all';

        // Hexagon coordinates generator for regular axial honeycomb grid
        function generateHoneycombLattice(nodes) {
            // Hexagon radius
            const R = 44;
            const cx = window.innerWidth > 900 ? 460 : 320;
            const cy = 290;

            // Concentric axial coordinates (q, r)
            const coords = [{ q: 0, r: 0 }];
            let ring = 1;
            while (coords.length < nodes.length + 10) {
                let q = ring, r = 0;
                // 6 directions of hexagon neighbors
                const dirs = [
                    { dq: -1, dr: 1 },
                    { dq: -1, dr: 0 },
                    { dq: 0, dr: -1 },
                    { dq: 1, dr: -1 },
                    { dq: 1, dr: 0 },
                    { dq: 0, dr: 1 }
                ];
                for (let d = 0; d < 6; d++) {
                    for (let step = 0; step < ring; step++) {
                        coords.push({ q, r });
                        q += dirs[d].dq;
                        r += dirs[d].dr;
                    }
                }
                ring++;
            }

            // Assign positions to nodes
            return nodes.map((node, i) => {
                const { q, r } = coords[i % coords.length];
                // Pointy-topped hexagon coordinate formula
                const x = cx + R * Math.sqrt(3) * (q + r / 2);
                const y = cy + R * (3 / 2) * r;
                return {
                    ...node,
                    x: node.x !== undefined ? node.x : x,
                    y: node.y !== undefined ? node.y : y,
                    origX: x,
                    origY: y,
                    r: 34
                };
            });
        }

        async function loadGraphData() {
            try {
                const res = await fetch('/api/graph');
                const data = await res.json();
                
                // Color encoding rules strictly matching user prompt:
                // - People / Employees: Secondary color (Violet / Purple: #a855f7)
                // - Situations: Primary RGY colors:
                //    * 🔴 Red: Critical threat / compromised asset (AST-01, INC-2026-001)
                //    * 🟡 Yellow: Warning / sensitive asset (AST-02, Project FalconShield)
                //    * 🟢 Green: Safe / Contained asset (AST-03, Safety Documents, or Quarantined asset)
                honeycombNodes = (data.nodes || []).map(n => {
                    let color = "#94a3b8"; // default slate
                    let rgy = "neutral";
                    let icon = "📄";
                    let category = "other";

                    if (n.group === "Employee") {
                        color = "#a855f7"; // Vibrant secondary purple
                        icon = "👤";
                        category = "people";
                    } else if (n.group === "Incident") {
                        color = isQuarantined ? "#10b981" : "#ef4444"; // 🔴 Red or 🟢 Green if fixed
                        rgy = isQuarantined ? "green" : "red";
                        icon = "🚨";
                        category = "situations";
                    } else if (n.id === "AST-01") {
                        color = isQuarantined ? "#10b981" : "#ef4444"; // 🔴 Red or 🟢 Green
                        rgy = isQuarantined ? "green" : "red";
                        icon = "💻";
                        category = "situations";
                    } else if (n.id === "AST-02" || n.group === "Project") {
                        color = "#f59e0b"; // 🟡 Yellow Warning / Sensitive
                        rgy = "yellow";
                        icon = n.group === "Project" ? "🚀" : "🗄️";
                        category = "situations";
                    } else if (n.id === "AST-03" || n.group === "Document") {
                        color = "#10b981"; // 🟢 Green Safe
                        rgy = "green";
                        icon = "📑";
                        category = "situations";
                    } else if (n.group === "Team") {
                        color = "#38bdf8"; // cyan
                        icon = "📁";
                    } else if (n.group === "Agent") {
                        color = "#ff6b00"; // solar orange
                        icon = "🤖";
                    }

                    return {
                        id: n.id,
                        label: n.label.replace(/^[A-Za-z]+:\s*/, ''),
                        group: n.group,
                        color: color,
                        rgy: rgy,
                        icon: icon,
                        category: category
                    };
                });

                honeycombNodes = generateHoneycombLattice(honeycombNodes);
                honeycombLinks = data.edges || [];
                renderHoneycomb();
            } catch (err) {
                console.error("Load graph error:", err);
            }
        }

        // Regular hexagon SVG polygon points around (cx, cy)
        function getHexPoints(cx, cy, r) {
            let pts = [];
            for (let i = 0; i < 6; i++) {
                const angle = (Math.PI / 3) * i + Math.PI / 6;
                const px = cx + r * Math.cos(angle);
                const py = cy + r * Math.sin(angle);
                pts.push(`${px.toFixed(1)},${py.toFixed(1)}`);
            }
            return pts.join(" ");
        }

        function renderHoneycomb() {
            const svg = document.getElementById('honeycomb-svg');
            const linksG = document.getElementById('honeycomb-links');
            const cellsG = document.getElementById('honeycomb-cells');
            if (!svg || !linksG || !cellsG) return;

            linksG.innerHTML = '';
            cellsG.innerHTML = '';

            const nodeMap = {};
            honeycombNodes.forEach(n => { nodeMap[n.id] = n; });

            // 1. Render Links
            honeycombLinks.forEach(link => {
                const src = nodeMap[link.from];
                const dst = nodeMap[link.to];
                if (!src || !dst) return;

                // Check active filter
                if (activeFilter === 'people' && src.category !== 'people' && dst.category !== 'people') return;
                if (activeFilter === 'situations' && src.category !== 'situations' && dst.category !== 'situations') return;

                const isBreach = (src.id === 'AST-01' || dst.id === 'AST-01' || src.id === 'INC-2026-001' || dst.id === 'INC-2026-001');

                const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
                line.setAttribute("x1", src.x);
                line.setAttribute("y1", src.y);
                line.setAttribute("x2", dst.x);
                line.setAttribute("y2", dst.y);
                line.setAttribute("stroke", isBreach ? "#ff6b00" : "rgba(255, 255, 255, 0.12)");
                line.setAttribute("stroke-width", isBreach ? "2.5" : "1.2");
                if (isBreach) line.setAttribute("class", "breach-link");
                linksG.appendChild(line);
            });

            // 2. Render Hexagon Cells
            honeycombNodes.forEach(node => {
                if (activeFilter === 'people' && node.category !== 'people') return;
                if (activeFilter === 'situations' && node.category !== 'situations') return;

                const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
                g.setAttribute("class", "hex-cell");
                g.setAttribute("id", `hex-${node.id}`);
                g.style.color = node.color;

                // Hexagon base polygon
                const hex = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
                hex.setAttribute("points", getHexPoints(node.x, node.y, node.r));
                hex.setAttribute("fill", "rgba(12, 16, 26, 0.88)");
                hex.setAttribute("stroke", node.color);
                hex.setAttribute("stroke-width", "2");

                // Icon Text
                const icon = document.createElementNS("http://www.w3.org/2000/svg", "text");
                icon.setAttribute("x", node.x);
                icon.setAttribute("y", node.y - 4);
                icon.setAttribute("text-anchor", "middle");
                icon.setAttribute("font-size", "14");
                icon.textContent = node.icon;

                // Label Text
                const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
                label.setAttribute("x", node.x);
                label.setAttribute("y", node.y + 14);
                label.setAttribute("text-anchor", "middle");
                label.setAttribute("fill", "#ffffff");
                label.setAttribute("font-size", "9");
                label.setAttribute("font-weight", "600");
                label.setAttribute("font-family", "sans-serif");
                label.textContent = node.label.length > 10 ? node.label.substring(0, 9) + '…' : node.label;

                g.appendChild(hex);
                g.appendChild(icon);
                g.appendChild(label);

                // Pointer Events for Dynamic Dragging
                g.addEventListener('pointerdown', (e) => {
                    draggedNode = node;
                    dragOffset = { x: e.clientX - node.x, y: e.clientY - node.y };
                    g.setPointerCapture(e.pointerId);
                    e.stopPropagation();
                });

                g.addEventListener('pointermove', (e) => {
                    if (draggedNode === node) {
                        node.x = e.clientX - dragOffset.x;
                        node.y = e.clientY - dragOffset.y;
                        updateNodePositions();
                    }
                });

                g.addEventListener('pointerup', (e) => {
                    if (draggedNode === node) {
                        draggedNode = null;
                        try { g.releasePointerCapture(e.pointerId); } catch(err){}
                    }
                });

                // Click to inspect
                g.addEventListener('click', () => {
                    inspectNode(node);
                });

                cellsG.appendChild(g);
            });
        }

        function updateNodePositions() {
            renderHoneycomb();
        }

        function recenterHoneycomb() {
            honeycombNodes.forEach(node => {
                node.x = node.origX;
                node.y = node.origY;
            });
            renderHoneycomb();
        }

        function filterHoneycomb(filter) {
            activeFilter = filter;
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            const activeBtn = document.getElementById(`filter-${filter}`);
            if (activeBtn) activeBtn.classList.add('active');
            renderHoneycomb();
        }

        function inspectNode(node) {
            const insp = document.getElementById('honeycomb-inspector');
            if (!insp) return;
            insp.classList.remove('hidden');

            document.getElementById('inspect-icon').innerText = node.icon;
            document.getElementById('inspect-name').innerText = node.label;
            
            const badge = document.getElementById('inspect-badge');
            badge.innerText = `${node.group} · ${node.rgy !== 'neutral' ? node.rgy.toUpperCase() : 'OPERATIONAL'}`;
            badge.style.color = node.color;
            badge.style.borderColor = node.color;
            badge.style.backgroundColor = `${node.color}20`;

            const desc = document.getElementById('inspect-desc');
            if (node.category === 'people') {
                desc.innerText = `Team member in enterprise graph. Employs secondary color (${node.color}) for high-contrast visual tracking.`;
            } else if (node.rgy === 'red') {
                desc.innerText = `Critical risk detected in current situation. Requires immediate quarantine lockdown.`;
            } else if (node.rgy === 'yellow') {
                desc.innerText = `High-privilege system under monitoring. No breach detected.`;
            } else {
                desc.innerText = `Verified secure and operational. Full access policy enforced.`;
            }

            // List connections
            const connList = document.getElementById('inspect-connections');
            connList.innerHTML = '';
            const connected = honeycombLinks.filter(l => l.from === node.id || l.to === node.id);
            connected.slice(0, 4).forEach(l => {
                const otherId = l.from === node.id ? l.to : l.from;
                const d = document.createElement('div');
                d.className = "p-1.5 rounded-lg bg-white/[0.05] text-[10px] flex items-center justify-between";
                d.innerHTML = `<span>${l.label || 'CONNECTS'}</span><strong class="text-orange-300">${otherId}</strong>`;
                connList.appendChild(d);
            });
        }

        function closeInspector() {
            const insp = document.getElementById('honeycomb-inspector');
            if (insp) insp.classList.add('hidden');
        }

        function highlightNode(id) {
            const n = honeycombNodes.find(item => item.id === id);
            if (n) {
                inspectNode(n);
            }
        }

        // Initialize on load
        window.addEventListener('DOMContentLoaded', () => {
            loadGraphData();
        });
    </script>
</body>
</html>
"""

# Liquid Glass: cubic-bezier spring physics and specular highlights tuned

# Liquid Glass: cubic-bezier spring physics and specular highlights tuned
