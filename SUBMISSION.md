# 🛡️ SCOUT: Autonomous Enterprise Knowledge & Security Investigator

> **Official Submission for [WeMakeDevs & FalkorDB Graph Hacks 2026](https://www.wemakedevs.org/hackathons/falkordb/schedule)**  
> **Tracks Entered:** Track 1 (Graph-Powered Action Agent) · Track 2 (Agent Memory & Cross-Session Learning) · Track 3 (The Company Brain)  
> **Repository:** [github.com/CARLEELTECH0/scout-falkordb](https://github.com/CARLEELTECH0/scout-falkordb)

---

## 💡 Tagline & Elevator Pitch
**Scout unifies enterprise hierarchy, agent episodic memory, and autonomous incident containment into a single ultra-fast FalkorDB knowledge graph — transforming security operations from disconnected silos into explainable, sub-millisecond graph intelligence.**

---

## 🚨 The Problem: The Enterprise Data Silo Crisis
In modern enterprises, security and IT incident response is crippled by fragmented data:
* **Organizational Data** lives in Active Directory or Workday.
* **Infrastructure Maps** reside in AWS/GCP or Kubernetes manifests.
* **Audit & Security Telemetry** streams into Splunk or Datadog.
* **Incident Response Runbooks** sit dormant in Confluence or Notion.

When a critical breach occurs (e.g. brute-force attack or anomalous bulk egress), security analysts waste hours manually pivoting across these disparate tools to answer three fundamental questions:
1. *Which infrastructure assets are affected?*
2. *Who accessed them, who do they report to, and which confidential projects are downstream?*
3. *What procedural playbook or memory worked the last time we saw this threat?*

---

## ⚡ The Solution: Scout on FalkorDB
Scout replaces fragmented tables and disconnected dashboards with a **unified property graph in FalkorDB**. Every employee, team, project, infrastructure asset, log event, agent conversation, and procedural memory node lives in the same graph database.

By leveraging **FalkorDB's C-based GraphBLAS matrix multiplication engine**, Scout traverses multi-hop relationships in **sub-millisecond latencies (<2ms)**, enabling autonomous AI agents to reason, triage, and contain threats in real-time.

---

## 🏆 Hackathon Track Coverage

### 🎯 Track 1: Graph-Powered Action Agent (`scout/agent.py`)
* **Multi-Hop Autonomous Reasoning**: Executes 4-hop Cypher traversals across incidents, logs, assets, and procedural solutions to make explainable mitigation decisions.
* **Dynamic Tool Selection & Execution**: Autonomously triggers mitigation tools in the graph:
  - `TOOL-02 (FirewallQuarantine)`: Isolates compromised servers and databases.
  - `TOOL-04 (TokenRevocationEngine)`: Revokes leaked OAuth credentials and session tokens.
  - `TOOL-03 (GraphBlastRadiusAnalyzer)`: Traces downstream organizational exposure.
* **Automated Log Triage**: Analyzes live telemetry streams, creates `Incident` nodes, connects them to root-cause `Log` and target `Asset` nodes, and initiates lockdown.

### 🧠 Track 2: Agent Memory & Cross-Session Learning (`scout/memory.py`)
* **Episodic Conversation & Decision Memory**: Stores chronological agent interactions, prompts, responses, and session contexts in FalkorDB (`Session` and `Interaction` nodes).
* **Semantic Concept & Procedural Recall**: Links past successful remediation actions to generalized security concepts (`BruteForceSpike`, `DataExfiltrationRisk`, `ClusterHealth`) via `(:RECALLS)` relationships. When a new threat emerges, agents query past playbooks before acting.
* **Multi-Agent Coordination & Task Handoffs**: When a task escalates (e.g. from `Scout-Alpha` security investigator to `Scout-Beta` IAM remediator), the handoff is immutably recorded in the graph with reason, timestamp, and audit trail.

### 🏢 Track 3: The Company Brain (`scout/brain.py`)
* **Organizational Hierarchy & Clearances**: Traverses `(:REPORTS_TO)`, `(:MEMBER_OF)`, and `(:ASSIGNED_TO)` edges to map employees to management chains and project groups.
* **Multi-Hop Blast Radius Risk Scoring**: Computes the blast radius if an asset is breached:
  $$\text{Risk Score} = (\text{Tier Weight} \times 25) + (\text{Staff Exposed} \times 15) + (\text{Projects Exposed} \times 20)$$
* **Zero-Trust Access Path Audits**: Verifies multi-hop authorization paths between employees, access tokens, and production servers to identify anomalous lateral movement paths.

---

## 🚀 Performance Benchmarks (FalkorDB vs Reality)

We benchmarked FalkorDB traversal throughput using `scripts/benchmark.py`:

| Operation / Cypher Workload | Avg Latency | p95 Latency | Throughput |
| :--- | :--- | :--- | :--- |
| **Single-Node Indexed Lookup** | **0.33 ms** | 0.59 ms | **~3,000 ops/s** |
| **3-Hop Blast Radius Traversal** | **1.72 ms** | 3.07 ms | **~580 ops/s** |
| **Multi-Hop Access Path Audit** | **1.28 ms** | 2.43 ms | **~780 ops/s** |
| **Episodic Procedural Memory Recall** | **1.07 ms** | 1.87 ms | **~930 ops/s** |
| **End-to-End Triage & Containment** | **6.03 ms** | 9.41 ms | **~165 ops/s** |

---

## 🎨 Interactive Visualizer & Key Features

1. **Generative Honeycomb Canvas**:
   - Regular hexagonal cells mathematically mapped in an axial spiral coordinate system with interactive pan/zoom and dynamic relational edge tracking.
2. **Dynamic 3-Panel Side-by-Side Workspace**:
   - **Left**: Pop-Out Inspector Ledger (Telemetry footprint, risk meter, Cypher breadcrumbs, and 1-click quarantine).
   - **Center**: Generative Honeycomb Visualizer with threat pulse rings.
   - **Right**: Dual-stream AI Team Narrative (`Scout-Alpha` & `Policy-Beta`) with voice equalizers.
3. **Audit-Ready Evidence Exporter (`scout/exporter.py`)**:
   - 1-click download of cryptographic post-mortem bundles with SHA-256 integrity checksums, blast radius analysis, and audit provenance.
4. **Tactical Voice Synthesizer (`scout/audio.py`)**:
   - Browser Web Speech API alerts spoken in real-time during threat containment and operator directive exchanges with audio toggle (`🔊 Voice On` / `🔇 Muted`).
5. **24/7 SOC Threat Daemon (`run.py simulate`)**:
   - Continuously feeds multi-vector synthetic attacks into FalkorDB every N seconds to simulate live SOC operations.

---

## 🛠️ Quick Start & Evaluation Guide

### Option A: 1-Click Docker Compose (Recommended)
```bash
git clone https://github.com/CARLEELTECH0/scout-falkordb.git
cd scout-falkordb
docker compose up
```
Open **`http://localhost:8000`** in your browser.

### Option B: Native Virtualenv Setup
```bash
# 1. Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Seed graph and run test suite
python run.py seed
pytest tests/test_scout.py

# 3. Launch interactive dashboard
python run.py serve 8000
```

### Option C: Run Performance Benchmark
```bash
python3 scripts/benchmark.py
```

### Option D: Run 24/7 SOC Threat Daemon
```bash
python run.py simulate 15
```

---

## 👥 Authors & Acknowledgments
Built with ❤️ by **CARLEELTECH0** for the **WeMakeDevs & FalkorDB Graph Hacks 2026**.  
*Licensed under MIT.*
