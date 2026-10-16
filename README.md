# 🛡️ SCOUT: Autonomous Enterprise Knowledge & Security Investigator

> **Built for [Graph Hacks 2026](https://www.wemakedevs.org/hackathons/falkordb/schedule) (WeMakeDevs & FalkorDB)**  
> **Tracks Entered:** Track 1 (Action Agent), Track 2 (Agent Memory), Track 3 (Company Brain)

---

## 🌟 Overview
**Scout** is an autonomous AI enterprise knowledge and security investigator powered by **FalkorDB**. Traditional security and IT operations suffer from disconnected data: identity directories, infrastructure maps, project trackers, and audit logs live in separate silos. When a security anomaly or breach occurs, analysts spend hours manually connecting the dots across disparate databases.

**Scout unifies the enterprise into a living graph:**
1. **Track 3 (Company Brain):** Maps employees, reporting chains, teams, projects, sensitive documents, and tiered infrastructure.
2. **Track 2 (Agent Memory):** Maintains persistent episodic conversation history, semantic concept recall, and multi-agent coordination handoffs in FalkorDB.
3. **Track 1 (Action Agent):** Executes multi-hop reasoning over the graph, selects remediation tools via Cypher queries and MCP, and takes automated mitigation actions (e.g., quarantining assets and revoking permissions) with complete explainability.

---

## 🏛️ System Architecture


The database schema connects all three domains in a single, high-performance FalkorDB graph:

```
[Employee] ──(:REPORTS_TO)──> [Employee]
   │
   ├──(:MEMBER_OF)───> [Team]
   ├──(:ASSIGNED_TO)─> [Project] ──(:CONTAINS)──> [Document]
   └──(:ACCESSED)────> [Asset] <──(:AFFECTS)── [Incident] ──(:TRIGGERED_BY)──> [Log]
                          ▲                           ▲
                          │ (:QUARANTINED_BY)         │ (:INVESTIGATED)
                          │                           │
                      [Agent] ─────(:USED_TOOL)───> [Tool]
                         │
                         ├──(:HAS_SESSION)──> [Session] <──(:RECORDED_IN)── [Interaction]
                         │                                                       │
                         └──(:HANDED_OFF_TO)─> [Agent]                           └──(:RECALLS)─> [Concept]
```

### Node Types
* **Track 3 (Company Brain):** `Employee`, `Team`, `Project`, `Asset` (Server/Database), `Document`
* **Track 2 (Agent Memory):** `Agent`, `Session`, `Interaction`, `Concept`
* **Track 1 (Action Agent):** `Incident`, `Tool`, `Log`

### Edge Types
* `REPORTS_TO`: Org hierarchy
* `MEMBER_OF`: Team affiliation
* `ASSIGNED_TO`: Project allocation
* `ACCESSED`: Infrastructure telemetry access
* `CONTAINS`: Project documentation provenance
* `AFFECTS`: Incident targeting infrastructure
* `TRIGGERED_BY`: Incident triggered by telemetry log event
* `INVESTIGATED`: Agent forensic investigation
* `USED_TOOL`: Agent tool execution audit
* `HAS_SESSION`: Agent memory partition
* `RECORDED_IN`: Episodic interaction history
* `RECALLS`: Semantic concept association
* `HANDED_OFF_TO`: Multi-agent coordination transfer
* `QUARANTINED_BY`: Active infrastructure containment

---

## ⚡ Core Cypher Queries

### 1. Multi-Hop Organizational Blast Radius (Track 3)
```cypher
MATCH (a:Asset {id: $asset_id})
OPTIONAL MATCH (inc:Incident)-[:AFFECTS]->(a)
OPTIONAL MATCH (e:Employee)-[:ACCESSED]->(a)
OPTIONAL MATCH (e)-[:ASSIGNED_TO]->(p:Project)
OPTIONAL MATCH (p)-[:CONTAINS]->(d:Document)
RETURN a.name AS asset_name,
       a.tier AS tier,
       collect(DISTINCT e.name) AS exposed_employees,
       collect(DISTINCT p.name) AS affected_projects,
       collect(DISTINCT d.title) AS exposed_documents
```

### 2. Procedural & Graph-Based Concept Recall (Track 2)
```cypher
MATCH (c:Concept)
WHERE toLower(c.name) = toLower($concept_name)
MATCH (i:Interaction)-[:RECALLS]->(c)
MATCH (i)-[:RECORDED_IN]->(s:Session)<-[:HAS_SESSION]-(a:Agent)
OPTIONAL MATCH (a)-[:USED_TOOL]->(t:Tool)
RETURN a.name AS agent_name,
       collect(DISTINCT t.name) AS tools_used,
       collect(DISTINCT i.response) AS past_solutions
```

### 3. Multi-Hop Incident Context & Tool Correlation (Track 1)
```cypher
MATCH (inc:Incident {id: $incident_id})
OPTIONAL MATCH (inc)-[:TRIGGERED_BY]->(l:Log)
OPTIONAL MATCH (inc)-[:AFFECTS]->(asset:Asset)
OPTIONAL MATCH (emp:Employee)-[:ACCESSED]->(asset)
OPTIONAL MATCH (agent:Agent)-[:INVESTIGATED]->(inc)
OPTIONAL MATCH (agent)-[:USED_TOOL]->(tool:Tool)
RETURN inc.title AS Incident,
       asset.name AS AffectedAsset,
       collect(DISTINCT emp.name) AS Accessors,
       agent.name AS Investigator,
       collect(DISTINCT tool.name) AS ToolsUsed
```

---

## 🚀 Quickstart & Setup

### 1. Clone & Install
```bash
git clone <repo_url>
cd scout
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configuration (Zero-Config or Cloud)
Scout works **out-of-the-box with embedded zero-config FalkorDB** (`falkordblite`). No Docker or local server installation is needed!

To connect to a remote FalkorDB instance (e.g. FalkorDB Cloud), simply add to `.env`:
```env
FALKORDB_HOST=your-cluster-url.falkordb.cloud
FALKORDB_PORT=6379
FALKORDB_USERNAME=default
FALKORDB_PASSWORD=your_password
```

### 3. Run the Autonomous Demo
Execute the full multi-hop end-to-end investigation workflow:
```bash
python run.py demo
```

### 4. Launch the Interactive Web Dashboard
```bash
python run.py serve 8000
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser to view:
* The live FalkorDB interactive graph topology.
* Real-time multi-hop agent reasoning stream.
* Simulation button to trigger live authentication attacks.

---

## 🔌 Model Context Protocol (MCP) Integration
Scout can be plugged directly into Claude Code, Antigravity, Cursor, or Hermes as an MCP tool server:
```bash
python run.py mcp
```
Exposes tools:
* `scout_compute_blast_radius`
* `scout_investigate_incident`
* `scout_recall_memory`
* `scout_audit_access_path`
* `scout_quarantine_asset`

---

## 🎨 Modern Collaboration UI & Honeycomb Architecture

Scout features a modern, responsive enterprise operations workspace designed for real-time threat investigation and team collaboration:

1. **First Frame Focus**:
   - The workspace immediately surfaces the **AI Team Chat Stream & Current Situation Banner**.
   - Displays real-time reasoning and discussions between `Scout-Alpha` (Security Guardian) and `Policy-Beta` (Team & Rules Advisor).
   - Features playable audio voice note bubbles with animated soundwave equalizers and document attachments.

2. **Dynamic Honeycomb Lattice Graph**:
   - Interactive regular hexagon SVG cells arranged in an axial honeycomb spiral:
     $$x = \text{centerX} + R \cdot \sqrt{3} \cdot (q + r/2)$$
     $$y = \text{centerY} + R \cdot \frac{3}{2} \cdot r$$
   - Dynamic pointer-capture physics allowing fluid drag-and-drop manipulation of any hexagon node while relational edges smoothly track adjacent cells.

3. **Strict Color Architecture**:
   - **People / Employees**: Encoded in **Secondary Color** (Vibrant Violet `#a855f7`) for contrast against operational states.
   - **Situations & Threats**: Strictly mapped to **Primary RGY** (Red, Green, Yellow):
     - 🔴 **Red**: Critical risks and compromised assets (`prod-auth-gateway`, active brute force).
     - 🟡 **Yellow**: Elevated access and monitored assets (`prod-falcon-cluster`, `Project FalconShield`).
     - 🟢 **Green**: Operational, safe, or quarantined & contained assets (`analytics-warehouse`, and quarantined targets post-lockdown).

4. **Dynamic 3-Panel Side-by-Side Workspace**:
   - Seamless non-overlapping layout supporting concurrent triage:
     - **Left**: Pop-Out Inspector Ledger (Direct telemetry footprint, risk meter, Cypher multi-hop breadcrumbs, and 1-click quarantine).
     - **Center**: Generative Honeycomb Hero Canvas (Infinite pan/zoom, threat pulse rings, relational lineage tracing, and axial coordinates).
     - **Right**: Autonomous Agent Narrative (Dual-stream AI dialogue, voice synthesis equalizers, and operator directive console).

---

## ⚡ Live Attack Simulator & Audit Evidence Exporter

### Multi-Vector Threat Simulator (`scout/simulator.py`)
Scout includes a built-in multi-vector attack generator for real-time demonstrations:
* **`AUTH_BRUTE_FORCE`**: Distributed SSH & OAuth attack bursts against Tier-1 authentication gateways.
* **`BULK_DATA_EXFILTRATION`**: Anomalous outbound egress surges from internal database clusters.
* **`PRIVILEGE_ESCALATION`**: Kernel capability elevation and syscall breakouts on Kubernetes worker nodes.
* **`CREDENTIAL_STUFFING`**: Coordinated botnet authentication floods with leaked tokens.

Trigger an attack via UI (`⚡ Attack Surge`) or REST API:
```bash
curl -X POST http://localhost:8000/api/simulate/attack \
  -H "Content-Type: application/json" \
  -d '{"vector": "AUTH_BRUTE_FORCE"}'
```

### Audit-Ready Incident Evidence Bundle (`scout/exporter.py`)
Export audit-ready post-mortem evidence bundles with cryptographic verification:
```bash
curl -s http://localhost:8000/api/incidents/INC-2026-001/evidence
```
Includes:
* Cryptographic SHA-256 integrity checksum (verifiable via `EvidenceExporter.verify_bundle()`).
* Multi-hop Cypher traversal provenance and reasoning hops.
* Organizational blast radius, exposed staff, and affected project dependencies.
* Autonomous agent mitigation actions and FalkorDB episodic memory session tags.

### Tactical Voice & Audio Synthesizer (`scout/audio.py`)
Scout features real-time agent voice synthesis via browser Web Speech API and backend phonetics:
* **Tactical Call Signs**: `Scout-Alpha` (Security Guardian) and `Policy-Beta` (Compliance Advisor).
* **Live Audio Telemetry**: Automatic voice alerts during threat surges, containment actions, and human directive verifications.
* **Equalizer Soundwave Sync**: Visual soundwave equalizer animations synchronized with real-time agent speech.

---

## 🚀 Performance Benchmarks (FalkorDB Sub-Millisecond Traversal)

Run the included benchmark suite:
```bash
python3 scripts/benchmark.py
```

### Verified Empirical Benchmark Results
Measured directly against local FalkorDB engine over 100 iterations:

| Operation / Cypher Workload | Avg Latency | p95 Latency | Throughput |
| :--- | :--- | :--- | :--- |
| **Single-Node Indexed Lookup** | **0.37 ms** | 0.53 ms | **2,717 ops/s** |
| **3-Hop Blast Radius Traversal** | **1.69 ms** | 2.83 ms | **590 ops/s** |
| **Multi-Hop Credential & Access Path Audit** | **1.33 ms** | 2.32 ms | **750 ops/s** |
| **Episodic Procedural Memory Recall** | **1.43 ms** | 2.53 ms | **701 ops/s** |
| **End-to-End Multi-Hop Triage & Containment** | **7.21 ms** | 12.53 ms | **139 ops/s** |

---

## 🐳 1-Click Containerized Deployment (Docker Compose)

Launch the complete FalkorDB + Scout stack with a single command:
```bash
docker compose up
```
Open **`http://localhost:8000`** in your browser.

### 24/7 Background SOC Threat Daemon
Simulate continuous live security operations by generating background multi-vector attack events:
```bash
python run.py simulate 15
```

---

## 📑 Hackathon Resources & Documentation
* **[Official Submission Write-Up (`SUBMISSION.md`)](SUBMISSION.md)**: Complete problem analysis, track breakdown, and FalkorDB architectural design.
* **[3-Minute Video Demo Script (`DEMO_SCRIPT.md`)](DEMO_SCRIPT.md)**: Precise timestamped walkthrough and voiceover guide for recording.

---

## 📜 License
MIT License. Built for FalkorDB Graph Hacks 2026.


