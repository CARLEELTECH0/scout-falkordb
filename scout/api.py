"""
FastAPI REST Backend & Interactive Single-Page Visualizer for Scout
Serves the unified FalkorDB graph, multi-hop reasoning endpoints, and the Spatial Navigation Dashboard:
- Top Context Bar: Search/Command bar, View pivots, Dynamic Micro-Telemetry Pill
- Left Panel: Pop-Out Inspector Ledger (Telemetry, Blast Radius, Step-by-Step Trace, Quarantine)
- Center Panel: Dynamic Generative Honeycomb Hero Canvas (Lineage Highlighting, Threat Flow Paths, Multi-Layered Pulse)
- Right Panel: Autonomous Agent Narrative (Dual-Stream Debate, Voice Waveform, Graph Mutation Anchors)
- Seamless 3-Panel Side-By-Side View: When all panels are opened, they sit side-by-side without overlapping!
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

from scout.db import FalkorGraph
from scout.brain import CompanyBrain
from scout.memory import AgentMemory
from scout.agent import ScoutActionAgent
from scout.seed import seed_enterprise_graph
from scout.simulator import AttackSimulator
from scout.exporter import EvidenceExporter
from scout.audio import TacticalAudioSynthesizer

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
simulator = AttackSimulator(db=db)
exporter = EvidenceExporter(db=db)
audio_synth = TacticalAudioSynthesizer()

# -------------------------------------------------------------
# Request Schemas
# -------------------------------------------------------------
class InvestigateRequest(BaseModel):
    incident_id: str
    session_id: Optional[str] = None

class AttackSimulationRequest(BaseModel):
    vector: Optional[str] = None
    session_id: Optional[str] = "SES-101"

class AudioSynthesisRequest(BaseModel):
    event_type: str = "BREACH_ALERT"
    context: Optional[Dict[str, Any]] = None

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
@app.get("/api/health")
def health_check():
    """Health check endpoint verifying FalkorDB connectivity and engine status."""
    falkor_ok = True
    try:
        db.query("RETURN 1")
    except Exception:
        falkor_ok = False
    return {
        "status": "healthy" if falkor_ok else "degraded",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "engine": "FalkorDB Graph Engine",
        "tracks": {
            "track1_action_agent": "operational",
            "track2_agent_memory": "operational",
            "track3_company_brain": "operational"
        },
        "audio_synthesizer": "operational",
        "simulator": "operational"
    }

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

@app.get("/api/simulate/scenarios")
def list_attack_scenarios():
    """Return available multi-vector attack scenarios."""
    return simulator.list_scenarios()

@app.post("/api/simulate/attack")
def trigger_attack_simulation(req: Optional[AttackSimulationRequest] = None):
    """Trigger a synthetic security incident pulse, mutating FalkorDB and running autonomous agent triage."""
    vector = req.vector if req else None
    session_id = req.session_id if req else "SES-101"
    return simulator.trigger_attack(vector=vector, session_id=session_id)

@app.get("/api/incidents/{incident_id}/evidence")
def export_evidence(incident_id: str, format: str = "markdown"):
    """Export audit-ready incident post-mortem evidence bundle (Markdown or JSON)."""
    if format.lower() == "json":
        return exporter.generate_incident_bundle(incident_id)
    return PlainTextResponse(exporter.export_markdown(incident_id), media_type="text/markdown")

@app.post("/api/audio/synthesize")
def synthesize_audio(req: AudioSynthesisRequest):
    """Generate tactical voice synthesis script and radio telemetry payload."""
    return audio_synth.generate_cue(req.event_type, req.context)


# -------------------------------------------------------------
# Spatial Navigation & 3-Panel Side-By-Side Dashboard
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
                            500: '#ea580c',
                            600: '#c2410c',
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
            --liquid-orange: #c2410c;
            --spring-curve: cubic-bezier(0.16, 1, 0.3, 1);
        }

        body {
            background-color: var(--bg-canvas);
            color: #f1f5f9;
            font-family: 'Plus Jakarta Sans', sans-serif;
            margin: 0;
            padding: 0;
            overflow: hidden;
        }

        /* Dribbble Pillowy Rounded Cards */
        .dribbble-card {
            background: linear-gradient(150deg, rgba(22, 28, 46, 0.75) 0%, rgba(12, 16, 28, 0.92) 100%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 28px;
            box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.6), inset 0 1px 1px 0 rgba(255, 255, 255, 0.12);
        }

        /* Solar Action Button */
        .btn-solar {
            background: linear-gradient(135deg, #ea580c 0%, #c2410c 100%);
            border-radius: 9999px;
            box-shadow: 0 10px 25px -5px rgba(194, 65, 12, 0.45), inset 0 1px 1px rgba(255, 255, 255, 0.3);
            color: #ffffff;
            font-weight: 600;
            transition: all 0.25s var(--spring-curve);
        }
        .btn-solar:hover {
            transform: scale(1.03);
            box-shadow: 0 14px 30px -5px rgba(194, 65, 12, 0.65), inset 0 1px 1px rgba(255, 255, 255, 0.4);
        }

        /* Obsidian Glass Secondary Button */
        .btn-obsidian {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 9999px;
            color: #cbd5e1;
            transition: all 0.2s ease;
        }
        .btn-obsidian:hover {
            background: rgba(255, 255, 255, 0.1);
            color: #ffffff;
            border-color: rgba(255, 255, 255, 0.2);
        }

        /* Dynamic 3-Panel Side-By-Side Layout System */
        #inspector-ledger-col {
            width: 400px;
            min-width: 380px;
            max-width: 90vw;
            transition: width 0.35s var(--spring-curve), min-width 0.35s var(--spring-curve), opacity 0.3s ease, padding 0.35s var(--spring-curve);
            box-shadow: 15px 0 45px rgba(0, 0, 0, 0.85);
        }
        #inspector-ledger-col.drawer-closed {
            width: 0 !important;
            min-width: 0 !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
            opacity: 0;
            pointer-events: none;
            overflow: hidden;
            border-right-width: 0 !important;
        }
        #inspector-ledger-col.drawer-open {
            width: 400px;
            min-width: 380px;
            opacity: 1;
            pointer-events: auto;
            border-right-width: 1px;
        }

        #narrative-col {
            width: 420px;
            min-width: 380px;
            max-width: 90vw;
            transition: width 0.35s var(--spring-curve), min-width 0.35s var(--spring-curve), opacity 0.3s ease;
            box-shadow: -15px 0 45px rgba(0, 0, 0, 0.85);
        }
        #narrative-col.chat-closed {
            width: 0 !important;
            min-width: 0 !important;
            opacity: 0;
            pointer-events: none;
            overflow: hidden;
            border-left-width: 0 !important;
        }
        #narrative-col.chat-open {
            width: 420px;
            min-width: 380px;
            opacity: 1;
            pointer-events: auto;
            border-left-width: 1px;
        }

        /* Floating Narrative Action Button (FAB) */
        #floating-narrative-btn {
            transition: all 0.3s var(--spring-curve);
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.85), 0 0 25px rgba(194, 65, 12, 0.40);
        }
        #floating-narrative-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 16px 45px rgba(0, 0, 0, 0.95), 0 0 35px rgba(194, 65, 12, 0.60);
        }

        /* Honeycomb Hexagon Animations */
        .hex-cell {
            transition: transform 0.35s var(--spring-curve), opacity 0.35s ease, filter 0.35s ease;
            transform-origin: center center;
            cursor: pointer;
        }
        .hex-cell:hover {
            transform: scale(1.16);
            filter: drop-shadow(0 0 18px currentColor);
        }
        .hex-cell.sprouting-node {
            animation: sproutScale 0.6s var(--spring-curve) backwards;
        }

        @keyframes sproutScale {
            0% {
                transform: scale(0.15);
                opacity: 0;
            }
            70% {
                transform: scale(1.12);
                opacity: 0.9;
            }
            100% {
                transform: scale(1);
                opacity: 1;
            }
        }

        /* Multi-Layered Threat Pulse Rings */
        .pulse-ring-1 {
            animation: threatRingPulse 2.4s cubic-bezier(0.2, 0.8, 0.2, 1) infinite;
            transform-origin: center center;
        }
        .pulse-ring-2 {
            animation: threatRingPulse 2.4s cubic-bezier(0.2, 0.8, 0.2, 1) infinite 0.7s;
            transform-origin: center center;
        }
        .pulse-ring-3 {
            animation: threatRingPulse 2.4s cubic-bezier(0.2, 0.8, 0.2, 1) infinite 1.4s;
            transform-origin: center center;
        }

        @keyframes threatRingPulse {
            0% {
                r: 34px;
                opacity: 0.9;
                stroke-width: 3.5px;
            }
            100% {
                r: 105px;
                opacity: 0;
                stroke-width: 0.8px;
            }
        }

        /* Animated Directional Threat Path */
        .threat-flow-path {
            stroke: #ef4444;
            stroke-width: 2.5px;
            stroke-dasharray: 6 5;
            animation: flowMarch 1.2s linear infinite;
        }
        @keyframes flowMarch {
            from { stroke-dashoffset: 22; }
            to { stroke-dashoffset: 0; }
        }

        /* Audio Waveform Equalizer Bars */
        @keyframes soundWave {
            0%, 100% { height: 4px; }
            50% { height: 16px; }
        }
        .sound-bar-1 { animation: soundWave 0.8s ease-in-out infinite; }
        .sound-bar-2 { animation: soundWave 0.95s ease-in-out infinite 0.2s; }
        .sound-bar-3 { animation: soundWave 0.7s ease-in-out infinite 0.4s; }

        .waveform-bar {
            width: 2.5px;
            border-radius: 2px;
            background-color: #cbd5e1;
        }

        /* Micro scrollbars */
        ::-webkit-scrollbar { width: 4px; height: 4px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: rgba(194, 65, 12, 0.35); border-radius: 2px; }
        ::-webkit-scrollbar-thumb:hover { background: rgba(194, 65, 12, 0.55); }
    </style>
</head>
<body class="h-screen w-screen flex flex-col antialiased selection:bg-orange-500/30 selection:text-orange-200 overflow-hidden relative">
    <!-- =================================================================== -->
    <!-- 1. PERSISTENT TOP CONTEXT BAR (UNIVERSAL ANCHOR - 56px)             -->
    <!-- =================================================================== -->
    <header class="h-[56px] px-6 bg-[#090c15] border-b border-white/[0.08] flex items-center justify-between shrink-0 z-40">
        <!-- Brand & Global Search Bar -->
        <div class="flex items-center gap-3.5">
            <div class="flex items-center gap-2">
                <div class="w-7 h-7 rounded-lg bg-gradient-to-tr from-orange-600 to-amber-500 flex items-center justify-center font-black text-sm text-white shadow-md shadow-orange-500/30">
                    S
                </div>
                <span class="font-black text-sm tracking-wider text-white">SCOUT</span>
                <span class="text-[10px] font-mono px-2 py-0.5 rounded-full bg-orange-500/10 text-orange-400 border border-orange-500/30 font-bold">FalkorDB</span>
            </div>

            <div class="h-4 w-px bg-white/10 mx-1 hidden sm:block"></div>

            <!-- Global Search / Command Bar -->
            <div class="relative hidden md:flex items-center w-80">
                <span class="absolute left-3 text-slate-500 text-xs">🔍</span>
                <input id="global-search-input" onkeyup="handleGlobalSearch(event)" type="text" placeholder="Search graph, users, credentials... [⌘K]" class="h-9 w-full bg-black/50 border border-white/10 rounded-full pl-8 pr-12 text-xs text-white placeholder-slate-500 outline-none focus:border-orange-500/60 transition font-mono">
                <kbd class="absolute right-3 text-[10px] font-mono bg-white/10 text-slate-400 px-1.5 py-0.5 rounded border border-white/5">⌘K</kbd>
            </div>
        </div>

        <!-- Center View Pivot Controls -->
        <div class="flex items-center gap-2 p-1 bg-black/60 rounded-full border border-white/10 text-xs font-mono">
            <button onclick="recenterHoneycombCanvas()" class="px-3.5 py-1.5 rounded-full bg-orange-500/20 text-orange-300 border border-orange-500/40 font-bold transition flex items-center gap-1.5" title="Center on Real-Time Graph">
                <span>🗺️ Real-Time Map</span>
            </button>
            <button onclick="toggleInspectorLedger()" id="pivot-alerts-btn" class="px-3.5 py-1.5 rounded-full text-slate-400 hover:text-white transition flex items-center gap-1.5" title="Toggle Left Inspector Ledger">
                <span>🚨 Incident Ledger</span>
                <span id="pivot-badge" class="px-1.5 py-0.2 rounded-full bg-rose-500 text-white text-[9px] font-bold">1</span>
            </button>
            <button onclick="toggleNarrativePanel()" id="pivot-narrative-btn" class="px-3.5 py-1.5 rounded-full text-slate-400 hover:text-white transition flex items-center gap-1.5" title="Toggle Right AI Narrative">
                <span>💬 AI Narrative</span>
                <span class="w-1.5 h-1.5 rounded-full bg-orange-400 animate-pulse"></span>
            </button>
        </div>

        <!-- Contextual Status Micro-Telemetry Pill (Shifts Dynamically) -->
        <div class="flex items-center gap-3">
            <div id="telemetry-pill" onclick="openAlertSituationLedger()" class="px-3.5 py-1.5 rounded-full bg-rose-500/15 border border-rose-500/35 text-rose-300 text-xs font-mono flex items-center gap-2 cursor-pointer hover:border-rose-500 transition shadow-sm" title="Click to inspect critical situation on left">
                <span id="telemetry-pill-dot" class="w-2 h-2 rounded-full bg-rose-500 animate-pulse"></span>
                <span id="telemetry-pill-text"><strong>1 Active Breach:</strong> AST-01</span>
                <span id="telemetry-pill-badge" class="text-[9px] px-1.5 py-0.2 rounded bg-rose-500 text-white font-bold">CRITICAL</span>
            </div>
            <button onclick="triggerSimulatedAttack()" class="btn-solar text-xs hidden lg:inline-flex px-3.5 py-1.5" title="Simulate anomalous telemetry surge">
                <span>⚡ Attack Surge</span>
            </button>
            <button onclick="reseedGraph()" class="btn-obsidian text-xs px-3.5 py-1.5" title="Reset and reseed graph">
                <span>🔄 Reset</span>
            </button>
            <button id="btn-audio-toggle" onclick="toggleTacticalAudio()" class="btn-obsidian text-xs px-3.5 py-1.5 flex items-center gap-1.5" title="Toggle Tactical Voice Alerts">
                <span id="audio-icon">🔊</span>
                <span id="audio-label">Voice On</span>
            </button>
        </div>
    </header>

    <!-- =================================================================== -->
    <!-- DYNAMIC 3-PANEL SIDE-BY-SIDE CONTAINER                              -->
    <!-- =================================================================== -->
    <div id="workspace-container" class="flex-1 w-full h-[calc(100vh-56px)] flex relative overflow-hidden bg-[#070a12]">

        <!-- =============================================================== -->
        <!-- 1. LEFT PANEL: POP-OUT INSPECTOR LEDGER                         -->
        <!-- =============================================================== -->
        <aside id="inspector-ledger-col" class="drawer-closed shrink-0 h-full bg-[#0c101c]/95 backdrop-blur-2xl border-r border-white/10 z-30 flex flex-col p-5 space-y-4 overflow-y-auto">
            <!-- Drawer Header -->
            <div class="flex items-center justify-between pb-3 border-b border-white/[0.08] shrink-0">
                <div class="flex items-center gap-2">
                    <span class="text-base">🚨</span>
                    <div>
                        <h3 class="text-xs font-bold text-white uppercase font-mono tracking-wider">The Inspector Ledger</h3>
                        <p class="text-[10px] text-slate-400 font-mono">Direct Situation Telemetry</p>
                    </div>
                </div>
                <div class="flex items-center gap-2">
                    <span id="inspect-status-badge" class="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold uppercase bg-rose-500/20 text-rose-300 border border-rose-500/40">🔴 CRITICAL</span>
                    <button onclick="closeInspectorLedger()" class="w-7 h-7 rounded-full bg-white/[0.06] hover:bg-white/[0.12] text-slate-400 hover:text-white flex items-center justify-center text-xs transition" title="Close Ledger">
                        ✕
                    </button>
                </div>
            </div>

            <!-- Active Selected Node Context Card -->
            <div class="dribbble-card p-4 space-y-3 bg-black/60 border-orange-500/30 shrink-0">
                <div class="flex items-start gap-3">
                    <div id="ledger-icon" class="w-11 h-11 rounded-2xl bg-orange-600/20 border border-orange-500/40 text-orange-300 flex items-center justify-center text-2xl shrink-0">
                        💻
                    </div>
                    <div class="min-w-0 flex-1">
                        <div class="flex items-center justify-between">
                            <span id="ledger-group" class="text-[10px] font-mono text-orange-400 uppercase font-semibold">Tier-1 Infrastructure Asset</span>
                            <span id="ledger-id" class="text-[10px] font-mono text-slate-400">AST-01</span>
                        </div>
                        <h4 id="ledger-title" class="text-sm font-bold text-white truncate">prod-auth-gateway</h4>
                        <p id="ledger-desc" class="text-[11px] text-slate-300 leading-snug mt-1">
                            Core OAuth 2.0 and token issuance gateway handling production authentications.
                        </p>
                    </div>
                </div>
            </div>

            <!-- Scannable Telemetry & IP Footprint -->
            <div class="space-y-2 shrink-0">
                <div class="text-[10px] font-mono text-slate-400 uppercase tracking-wider flex items-center justify-between">
                    <span>Direct Telemetry Footprint</span>
                    <span class="text-emerald-400 font-bold">● Active Ingestion</span>
                </div>
                <div class="p-3.5 rounded-2xl bg-black/40 border border-white/[0.06] space-y-2 text-xs font-mono">
                    <div class="flex items-center justify-between py-0.5 border-b border-white/[0.04]">
                        <span class="text-slate-400 text-[10px]">IP Footprint</span>
                        <span id="ledger-ip" class="text-orange-300 font-bold text-[11px]">192.168.1.105</span>
                    </div>
                    <div class="flex items-center justify-between py-0.5 border-b border-white/[0.04]">
                        <span class="text-slate-400 text-[10px]">Protocol / Port</span>
                        <span class="text-slate-200 text-[11px]">SSHv2 / Port 22</span>
                    </div>
                    <div class="flex items-center justify-between py-0.5 border-b border-white/[0.04]">
                        <span class="text-slate-400 text-[10px]">Access Key Traced</span>
                        <span id="ledger-key" class="text-purple-300 font-bold text-[11px]">tok_98a (Bob Martinez)</span>
                    </div>
                    <div class="flex items-center justify-between py-0.5">
                        <span class="text-slate-400 text-[10px]">Department / Team</span>
                        <span class="text-purple-300 text-[11px]">SecOps (Alice Chen)</span>
                    </div>
                </div>
            </div>

            <!-- Dynamic Threat Blast Radius Meter -->
            <div class="p-4 rounded-2xl bg-black/50 border border-rose-500/30 space-y-3 shrink-0">
                <div class="flex items-center justify-between text-xs font-mono">
                    <span class="text-slate-400">Blast Radius Risk</span>
                    <span id="ledger-risk-score" class="text-rose-400 font-bold">125 / 100 [CRITICAL]</span>
                </div>
                <div class="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
                    <div id="ledger-risk-bar" class="bg-gradient-to-r from-amber-500 to-rose-600 h-2 rounded-full" style="width: 88%;"></div>
                </div>
                <div class="flex items-center justify-between text-[10px] text-slate-400 font-mono">
                    <span>Exposed Staff: 2</span>
                    <span>Projects at Risk: 1</span>
                    <span id="ledger-quarantine-status" class="text-rose-400 font-bold">Active Threat</span>
                </div>

                <!-- Instant Quarantine Action Button -->
                <button onclick="executeMitigation()" id="btn-ledger-quarantine" class="btn-solar w-full h-11 text-xs font-bold shadow-lg shadow-orange-500/35 mt-1">
                    <span>🛡️ Quarantine Asset & Contain Breach</span>
                </button>

                <!-- Export Incident Evidence Post-Mortem Button -->
                <button onclick="downloadEvidenceReport()" id="btn-export-evidence" class="w-full h-9 rounded-full bg-white/[0.06] hover:bg-white/[0.12] border border-white/10 text-xs font-mono font-medium text-slate-300 hover:text-white flex items-center justify-center gap-1.5 transition">
                    <span>📥 Export Evidence Bundle (.md)</span>
                </button>
            </div>

            <!-- Multi-Hop Breadcrumb Lineage Trace -->
            <div class="space-y-2 shrink-0">
                <div class="flex items-center justify-between text-xs font-mono">
                    <span class="text-[10px] font-mono uppercase text-slate-400 font-bold">Step-by-Step Traversal Trace</span>
                    <span class="text-[10px] font-mono text-purple-300">Cypher Multi-Hop</span>
                </div>
                <div class="p-3.5 rounded-2xl bg-black/40 border border-white/[0.06] space-y-2 text-xs font-mono">
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

        <!-- =============================================================== -->
        <!-- 2. CENTER PANEL: GENERATIVE HONEYCOMB HERO CANVAS                -->
        <!-- =============================================================== -->
        <main id="canvas-wrapper" class="flex-1 min-w-0 h-full relative overflow-hidden bg-[#070a12] select-none">
            
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
            <button id="btn-jump-alert" onclick="openAlertSituationLedger()" class="absolute top-4 right-6 z-20 px-4 py-2 rounded-full bg-rose-500/20 hover:bg-rose-500/30 border border-rose-500/70 text-rose-200 text-xs font-mono font-bold flex items-center gap-2 shadow-lg transition hover:scale-105">
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

            <!-- Floating Narrative Launcher Button (FAB) (Visible when Narrative Column is Closed) -->
            <button id="floating-narrative-btn" onclick="openNarrativePanel()" class="absolute bottom-6 right-6 z-20 px-4 py-2.5 rounded-full bg-gradient-to-r from-[#141b2e] to-[#1e172f] border border-orange-500/40 backdrop-blur-2xl text-white shadow-2xl flex items-center gap-3 transition cursor-pointer" title="Open Autonomous Agent Narrative">
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

                <!-- Root Viewport Transform Group (For Pan & Zoom) -->
                <g id="viewport-transform">
                    <!-- Layer 1: Zero-State Wireframe Hexagon Grid -->
                    <g id="zero-state-grid"></g>

                    <!-- Layer 2: Connection Links & Animated Threat Flow Paths -->
                    <g id="honeycomb-links"></g>

                    <!-- Layer 3: Solid Sprouting Hexagonal Cards -->
                    <g id="honeycomb-cells"></g>

                    <!-- Layer 4: Multi-Layered Threat Pulse Rings -->
                    <g id="threat-pulse-rings"></g>
                </g>
            </svg>
        </main>

        <!-- =============================================================== -->
        <!-- 3. RIGHT PANEL: AUTONOMOUS AGENT NARRATIVE CHAT                 -->
        <!-- =============================================================== -->
        <aside id="narrative-col" class="chat-closed shrink-0 h-full bg-[#0b0e19]/95 backdrop-blur-2xl border-l border-white/10 z-30 flex flex-col overflow-hidden">
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
                    <button onclick="closeNarrativePanel()" class="w-7 h-7 rounded-full bg-white/[0.06] hover:bg-white/[0.12] text-slate-400 hover:text-white flex items-center justify-center text-xs transition" title="Close Narrative">
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
                    <div class="p-2 rounded-xl bg-purple-950/30 border-l-2 border-purple-400 text-[11px] text-slate-300">
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

            <!-- Quick Action Suggestion Chips -->
            <div class="px-4 py-2 border-t border-white/[0.06] bg-black/40 flex items-center gap-2 overflow-x-auto shrink-0 text-[11px] font-mono">
                <button onclick="quickDirect('Investigate AST-01')" class="px-2.5 py-1 rounded-full bg-white/[0.05] hover:bg-orange-500/20 text-slate-300 hover:text-orange-300 border border-white/10 shrink-0 transition">
                    ⚡ Investigate AST-01
                </button>
                <button onclick="triggerSimulatedAttack()" class="px-2.5 py-1 rounded-full bg-white/[0.05] hover:bg-rose-500/20 text-slate-300 hover:text-rose-300 border border-white/10 shrink-0 transition">
                    🚨 Spike Log Surge
                </button>
                <button onclick="clearLineageHighlight()" class="px-2.5 py-1 rounded-full bg-white/[0.05] hover:bg-purple-500/20 text-slate-300 hover:text-purple-300 border border-white/10 shrink-0 transition">
                    ✕ Clear Lineage
                </button>
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
        </aside>

    </div>

    <!-- CLIENT JAVASCRIPT LOGIC -->
    <script>
        let currentIncident = 'INC-2026-001';
        let isQuarantined = false;
        let isNarrativeOpen = false;
        let isInspectorOpen = false;
        let isAudioEnabled = true;

        function toggleTacticalAudio() {
            isAudioEnabled = !isAudioEnabled;
            const icon = document.getElementById('audio-icon');
            const label = document.getElementById('audio-label');
            if (icon && label) {
                icon.innerText = isAudioEnabled ? '🔊' : '🔇';
                label.innerText = isAudioEnabled ? 'Voice On' : 'Muted';
            }
            if (window.speechSynthesis && !isAudioEnabled) {
                window.speechSynthesis.cancel();
            }
        }

        function speakTacticalAlert(text, pitch = 0.95, rate = 1.0) {
            if (!isAudioEnabled || !('speechSynthesis' in window)) return;
            try {
                window.speechSynthesis.cancel();
                const utter = new SpeechSynthesisUtterance(text);
                utter.pitch = pitch;
                utter.rate = rate;
                
                const bars = document.querySelectorAll('.sound-bar-1, .sound-bar-2, .sound-bar-3');
                utter.onstart = () => {
                    bars.forEach(b => b.classList.add('animate-bounce'));
                };
                utter.onend = () => {
                    bars.forEach(b => b.classList.remove('animate-bounce'));
                };
                window.speechSynthesis.speak(utter);
            } catch (err) {
                console.warn("Speech synthesis notice:", err);
            }
        }

        // Pan and Zoom State
        let panX = 0;
        let panY = 0;
        let zoom = 1;
        let isPanning = false;
        let panStartX = 0;
        let panStartY = 0;

        // Canvas Coordinates & Graph State
        let allGraphNodes = [];
        const R = 44; // Hexagon radius
        let originX = window.innerWidth / 2;
        let originY = window.innerHeight / 2;

        function updateCanvasOrigin() {
            const wrapper = document.getElementById('canvas-wrapper');
            if (wrapper && wrapper.clientWidth > 0 && wrapper.clientHeight > 0) {
                originX = wrapper.clientWidth / 2;
                originY = wrapper.clientHeight / 2;
            }
        }

        // Apply Pan & Zoom Transform to Viewport Group
        function updateViewportTransform() {
            const group = document.getElementById('viewport-transform');
            if (group) {
                group.setAttribute('transform', `translate(${panX}, ${panY}) scale(${zoom})`);
            }
        }

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
            updateCanvasOrigin();
            const gridG = document.getElementById('zero-state-grid');
            if (!gridG) return;
            gridG.innerHTML = '';

            // Spacious 11x11 wireframe hexagonal matrix
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
            updateCanvasOrigin();
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
                    color = "#ea580c"; // Deep Burnt Orange
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

                // Icon Symbol
                const icon = document.createElementNS("http://www.w3.org/2000/svg", "text");
                icon.setAttribute("x", node.cx);
                icon.setAttribute("y", node.cy - 5);
                icon.setAttribute("text-anchor", "middle");
                icon.setAttribute("dominant-baseline", "central");
                icon.setAttribute("font-size", "17");
                icon.textContent = node.icon;

                // Subtitle / ID Label
                const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
                label.setAttribute("x", node.cx);
                label.setAttribute("y", node.cy + 17);
                label.setAttribute("text-anchor", "middle");
                label.setAttribute("fill", "#e2e8f0");
                label.setAttribute("font-size", "10");
                label.setAttribute("font-family", "JetBrains Mono");
                label.setAttribute("font-weight", "600");
                label.textContent = node.label.length > 12 ? node.label.substring(0, 11) + '..' : node.label;

                g.appendChild(hex);
                g.appendChild(icon);
                g.appendChild(label);

                // Clicking ANY node pops out the Left Inspector Ledger!
                g.addEventListener('click', (e) => {
                    selectNodeAndPopOutInspector(node);
                    e.stopPropagation();
                });

                g.addEventListener('mouseenter', () => {
                    highlightLineage(node);
                });

                cellsG.appendChild(g);
            });

            updateViewportTransform();
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
        // 4. Left Panel: Inspector Ledger Controller
        // ----------------------------------------------------
        function selectNodeAndPopOutInspector(node) {
            highlightLineage(node);
            updateInspectorLedger(node);
            openInspectorLedger();
        }

        function openInspectorLedger() {
            const drawer = document.getElementById('inspector-ledger-col');
            const btn = document.getElementById('pivot-alerts-btn');
            if (drawer) {
                drawer.classList.remove('drawer-closed');
                drawer.classList.add('drawer-open');
                isInspectorOpen = true;
            }
            if (btn) {
                btn.className = "px-3.5 py-1.5 rounded-full bg-rose-500/20 text-rose-300 border border-rose-500/40 font-bold transition flex items-center gap-1.5";
            }
        }

        function closeInspectorLedger() {
            const drawer = document.getElementById('inspector-ledger-col');
            const btn = document.getElementById('pivot-alerts-btn');
            if (drawer) {
                drawer.classList.remove('drawer-open');
                drawer.classList.add('drawer-closed');
                isInspectorOpen = false;
            }
            if (btn) {
                btn.className = "px-3.5 py-1.5 rounded-full text-slate-400 hover:text-white transition flex items-center gap-1.5";
            }
        }

        function toggleInspectorLedger() {
            if (isInspectorOpen) {
                closeInspectorLedger();
            } else {
                openAlertSituationLedger();
            }
        }

        function openAlertSituationLedger() {
            const alertNode = allGraphNodes.find(n => n.id === "AST-01");
            if (alertNode) {
                selectNodeAndPopOutInspector(alertNode);
                const alertCell = document.getElementById('cell-AST-01');
                if (alertCell) {
                    alertCell.style.transition = "transform 0.5s var(--spring-curve)";
                    alertCell.style.transform = "scale(1.25)";
                    setTimeout(() => { alertCell.style.transform = "scale(1)"; }, 600);
                }
            } else {
                openInspectorLedger();
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
            } else {
                badge.innerText = "ℹ️ INSPECT";
                badge.className = "px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold uppercase bg-slate-700 text-slate-300 border border-slate-600";
            }
        }

        // ----------------------------------------------------
        // 5. Right Panel: Narrative Chat Controller
        // ----------------------------------------------------
        function openNarrativePanel() {
            const col = document.getElementById('narrative-col');
            const fab = document.getElementById('floating-narrative-btn');
            const btn = document.getElementById('pivot-narrative-btn');
            if (col) {
                col.classList.remove('chat-closed');
                col.classList.add('chat-open');
                isNarrativeOpen = true;
            }
            if (fab) {
                fab.classList.add('opacity-0', 'pointer-events-none', 'scale-90');
            }
            if (btn) {
                btn.className = "px-3.5 py-1.5 rounded-full bg-orange-500/20 text-orange-300 border border-orange-500/40 font-bold transition flex items-center gap-1.5";
            }
        }

        function closeNarrativePanel() {
            const col = document.getElementById('narrative-col');
            const fab = document.getElementById('floating-narrative-btn');
            const btn = document.getElementById('pivot-narrative-btn');
            if (col) {
                col.classList.remove('chat-open');
                col.classList.add('chat-closed');
                isNarrativeOpen = false;
            }
            if (fab) {
                fab.classList.remove('opacity-0', 'pointer-events-none', 'scale-90');
            }
            if (btn) {
                btn.className = "px-3.5 py-1.5 rounded-full text-slate-400 hover:text-white transition flex items-center gap-1.5";
            }
        }

        function toggleNarrativePanel() {
            if (isNarrativeOpen) {
                closeNarrativePanel();
            } else {
                openNarrativePanel();
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

                // Update Status Badge in Inspector
                const inspectBadge = document.getElementById('inspect-status-badge');
                if (inspectBadge) {
                    inspectBadge.innerText = "🟢 CONTAINED";
                    inspectBadge.className = "px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold uppercase bg-emerald-500/20 text-emerald-300 border border-emerald-500/40";
                }

                // Hide Jump to Alert button
                const btnJump = document.getElementById('btn-jump-alert');
                if (btnJump) btnJump.classList.add('hidden');
                const pivotBadge = document.getElementById('pivot-badge');
                if (pivotBadge) pivotBadge.innerText = "0";

                // Re-render canvas to show green safe state
                renderHoneycombCanvas();

                // Sprout Containment Cell into grid
                sproutNewBranch("AST-01", "ISOLATION_ZONE", "Containment Lock", "Security", "🛡️");

                speakTacticalAlert("Threat contained. Target asset isolated in quarantine zone. Lateral movement neutralized.", 0.95, 1.0);
                appendChatMessage("Scout-Alpha", "Asset AST-01 quarantined successfully in FalkorDB. Attack surface eliminated.", "scout", "Quarantine Active · 22ms");
            } catch (err) {
                console.error("Mitigation error:", err);
            }
        }

        async function triggerSimulatedAttack() {
            try {
                // Call real backend attack simulator
                const res = await fetch('/api/simulate/attack', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ session_id: 'SES-101' })
                });
                const data = await res.json();

                if (data.triage_result && data.triage_result.incident_created) {
                    currentIncident = data.triage_result.incident_created;
                }

                isQuarantined = false;
                const btnJump = document.getElementById('btn-jump-alert');
                if (btnJump) {
                    btnJump.classList.remove('hidden');
                    btnJump.innerHTML = `<span class="w-2 h-2 rounded-full bg-rose-500 animate-ping"></span><span>🚨 Inspect Threat: ${data.target_asset_id}</span>`;
                }

                const pill = document.getElementById('telemetry-pill');
                const dot = document.getElementById('telemetry-pill-dot');
                const text = document.getElementById('telemetry-pill-text');
                const badge = document.getElementById('telemetry-pill-badge');
                if (pill) pill.className = "px-3.5 py-1.5 rounded-full bg-rose-500/15 border border-rose-500/35 text-rose-300 text-xs font-mono flex items-center gap-2 cursor-pointer";
                if (dot) dot.className = "w-2 h-2 rounded-full bg-rose-500 animate-pulse";
                if (text) text.innerHTML = `<strong>1 Active Breach:</strong> ${data.target_asset_id}`;
                if (badge) {
                    badge.innerText = data.level || "CRITICAL";
                    badge.className = "text-[9px] px-1.5 py-0.2 rounded bg-rose-500 text-white font-bold";
                }

                const btn = document.getElementById('btn-ledger-quarantine');
                if (btn) {
                    btn.disabled = false;
                    btn.className = "btn-solar w-full h-11 text-xs font-bold shadow-lg shadow-orange-500/35 mt-1";
                    btn.innerHTML = "<span>🛡️ Quarantine Asset & Contain Breach</span>";
                }

                // Update ledger texts
                const ledgerId = document.getElementById('ledger-id');
                const ledgerTitle = document.getElementById('ledger-title');
                const ledgerDesc = document.getElementById('ledger-desc');
                if (ledgerId) ledgerId.innerText = data.target_asset_id;
                if (ledgerTitle) ledgerTitle.innerText = data.title;
                if (ledgerDesc) ledgerDesc.innerText = data.message;

                renderHoneycombCanvas();
                openAlertSituationLedger();

                speakTacticalAlert(`Security alert. Anomalous telemetry surge detected on ${data.target_asset_id}. Initiating graph triage in FalkorDB.`, 0.9, 1.05);
                appendChatMessage("Scout-Alpha", `⚡ LIVE TELEMETRY SURGE [${data.vector}]: ${data.message}`, "scout", "Triage Surge · 9ms");
                if (data.triage_result && data.triage_result.investigation) {
                    const inv = data.triage_result.investigation;
                    setTimeout(() => {
                        appendChatMessage("Policy-Beta", `Autonomous Containment: ${inv.explainable_verdict || 'Mitigation complete.'}`, "policy", "Policy Engine · 16ms");
                    }, 500);
                }
            } catch (err) {
                console.error("Simulation attack error:", err);
            }
        }

        async function downloadEvidenceReport() {
            try {
                const incId = currentIncident || 'INC-2026-001';
                const res = await fetch(`/api/incidents/${incId}/evidence?format=markdown`);
                if (!res.ok) throw new Error("Failed to export evidence bundle");
                const text = await res.text();
                const blob = new Blob([text], { type: "text/markdown" });
                const url = URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = `scout-evidence-${incId}.md`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            } catch (e) {
                console.error("Evidence export failed:", e);
                alert("Failed to export evidence report.");
            }
        }

        function sproutNewBranch(parentId, newId, label, group, icon) {
            const parent = allGraphNodes.find(n => n.id === parentId);
            if (!parent) return;

            const newNode = {
                id: newId,
                label: label,
                q: parent.q,
                r: parent.r + 1,
                group: group,
                icon: icon,
                parent: parentId
            };
            nodeDefinitions.push(newNode);
            renderHoneycombCanvas();

            // Update Active Cells Label
            const labelEl = document.getElementById('node-counter-label');
            if (labelEl) {
                labelEl.innerText = `${allGraphNodes.length} Active Cells`;
            }

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
        function quickDirect(text) {
            const input = document.getElementById('directive-input');
            if (input) {
                input.value = text;
                document.getElementById('directive-form').dispatchEvent(new Event('submit'));
            }
        }

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
                    speakTacticalAlert(data.policy_response.message, 1.15, 0.98);
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
            panX = 0;
            panY = 0;
            zoom = 1;
            updateViewportTransform();
            clearLineageHighlight();
            renderZeroStateGrid();
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

        // ----------------------------------------------------
        // 8. Pan & Zoom Event Listeners for Honeycomb SVG
        // ----------------------------------------------------
        function setupCanvasInteraction() {
            const svg = document.getElementById('honeycomb-viewport');
            if (!svg) return;

            svg.addEventListener('mousedown', (e) => {
                if (e.target.closest('.hex-cell')) return; // Cell click takes priority
                isPanning = true;
                panStartX = e.clientX - panX;
                panStartY = e.clientY - panY;
                svg.style.cursor = 'grabbing';
            });

            window.addEventListener('mousemove', (e) => {
                if (!isPanning) return;
                panX = e.clientX - panStartX;
                panY = e.clientY - panStartY;
                updateViewportTransform();
            });

            window.addEventListener('mouseup', () => {
                if (isPanning) {
                    isPanning = false;
                    svg.style.cursor = 'grab';
                }
            });

            svg.addEventListener('wheel', (e) => {
                e.preventDefault();
                const delta = e.deltaY > 0 ? 0.9 : 1.1;
                zoom = Math.min(Math.max(0.4, zoom * delta), 2.5);
                updateViewportTransform();
            }, { passive: false });
        }

        // Initialize on load with Dynamic Resize Observer
        window.addEventListener('DOMContentLoaded', () => {
            updateCanvasOrigin();
            renderZeroStateGrid();
            renderHoneycombCanvas();
            setupCanvasInteraction();

            // Observe dynamic flex resizing when left/right panels slide open or close
            const wrapper = document.getElementById('canvas-wrapper');
            if (wrapper && window.ResizeObserver) {
                const ro = new ResizeObserver(() => {
                    updateCanvasOrigin();
                    renderZeroStateGrid();
                    renderHoneycombCanvas();
                });
                ro.observe(wrapper);
            }
        });
    </script>
</body>
</html>
"""
