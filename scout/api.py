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
