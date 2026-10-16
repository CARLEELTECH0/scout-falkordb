# 🎬 SCOUT: Exact 3-Minute Video Demo & Walkthrough Plan

> **Title:** SCOUT — Investigate. Remember. Respond.  
> **Hackathon:** WeMakeDevs & FalkorDB Graph Hacks 2026  
> **Tracks Entered:**  
> • **Track 1:** Graph-Powered Action Agent  
> • **Track 2:** Agent Memory & Cross-Session Learning  
> • **Track 3:** The Company Brain  
> **Target Duration:** 3:00 Minutes (180 Seconds)  

---

## ⏱️ 1. The Video Storyboard & Exact Spoken Script

### Scene 1 — A Threat Appears (0:00 – 0:20 | 20 sec)
* **Screen View:** Scout dashboard at `http://localhost:8000`, then click **`⚡ Attack Surge`**.
* **Visual Action:** Watch the red threat pulse appear around `prod-auth-gateway`.
* **On-Screen Text Overlay:** `ONE THREAT. CONNECTED EVIDENCE.`
* **Spoken Narration:**
  > *"An enterprise security incident is rarely just one alert. The real challenge is understanding what was affected, who had access, what the organization could lose, and how to respond. I built Scout to investigate those connections using FalkorDB."*

---

### Scene 2 — Scout Connects the Dots (0:20 – 0:55 | 35 sec)
* **Screen View:** Honeycomb graph, `prod-auth-gateway`, connected assets, employees, projects, and documents.
* **Visual Action:**
  1. Click on node `AST-01` (`prod-auth-gateway`).
  2. Point the mouse to the lineage breadcrumbs (`Bob Martinez ➔ tok_98a ➔ prod-auth-gateway`).
  3. Show the blast-radius query and real-time Cypher traversal results in the Left Inspector Ledger.
* **On-Screen Text Overlay:** `TRACK 3 · COMPANY BRAIN`
* **Spoken Narration:**
  > *"Scout represents enterprise knowledge as a connected graph. Employees, teams, projects, documents, and infrastructure are linked through relationships. By traversing those relationships, Scout can investigate an asset's context and identify potentially affected people, projects, and documents."*

---

### Scene 3 — Investigation Becomes Action (0:55 – 1:35 | 40 sec)
* **Screen View:** Incident details, risk meter (`125/100 CRITICAL`), investigation narrative, then the containment button.
* **Visual Action:**
  1. Highlight the critical risk assessment and exposed staff.
  2. Click **`🛡️ Quarantine Asset & Contain Breach`**.
  3. Show the actual before-and-after state change in the graph (`🔴 CRITICAL` ➔ `🟢 CONTAINED`), the sprouted containment cell, and listen to the voice alert.
* **On-Screen Text Overlay:** `TRACK 1 · GRAPH-POWERED ACTION AGENT`
* **Spoken Narration:**
  > *"Scout correlates incident data, affected infrastructure, access relationships, and the tools used during investigation. It then exposes a containment workflow. When I trigger the quarantine action, you can see the resulting state change in Scout and its graph-backed data."*

---

### Scene 4 — The Memory Reveal (1:35 – 2:15 | 40 sec)
* **Screen View:** Right Panel AI Narrative (`#narrative-col`).
* **Visual Action:**
  1. Click **`💬 AI Narrative`** (or open the right panel).
  2. Click **`🧠 Retrieve Memory (Fresh Session)`**.
  3. Pause on the returned historical incident card showing:
     - New Session ID (`SES-XXXXXX`) initialized in FalkorDB.
     - Retrieved historical incident `INC-2026-001` (`BruteForceSpike`) on `prod-auth-gateway`.
     - Recalled procedural tools (`LogTelemetryScanner`, `FirewallQuarantine`).
     - Voice confirmation playing.
* **On-Screen Text Overlay:** `TRACK 2 · MEMORY THAT PERSISTS ACROSS SESSIONS`
* **Spoken Narration:**
  > *"But what happens when a new investigation begins? Does the agent have to start from scratch? Scout can initialize a fresh session and retrieve a previous Brute Force Spike incident from FalkorDB, including its connection to the affected gateway and the historical FirewallQuarantine playbook."*

---

### Scene 5 — Evidence and the Close (2:15 – 3:00 | 45 sec)
* **Screen View:** Top Bar `💾 Export Incident` ➔ Terminal running tests and Docker Compose.
* **Visual Action:**
  1. Click **`💾 Export Incident`** to show the real forensic evidence bundle download.
  2. Switch to terminal: show `python3 -m pytest tests/test_scout.py` passing **9/9 tests in 0.4s**.
  3. Show the 1-click `docker compose up` command in the terminal or README.
  4. End on the clean Scout dashboard interface and project title.
* **On-Screen Text Overlay:** `SCOUT — INVESTIGATE. REMEMBER. RESPOND.`
* **Spoken Narration:**
  > *"Scout brings together company knowledge, graph-based investigation, agent memory, and response workflows. It also includes an incident evidence exporter, an MCP interface, automated tests, and containerized deployment. The goal is to turn disconnected enterprise data into connected, explainable security investigations."*

---

## 🌟 2. What Makes This Demo Stand Out

The three tracks function as one continuous, cohesive workflow:
1. **First — The Graph Gives Scout Context (Track 3):**  
   Shows how assets connect to incidents, accessors, projects, and documents. This is where FalkorDB becomes central to the story.
2. **Second — Memory Gives Scout Continuity (Track 2):**  
   The fresh-session retrieval is more compelling than simply showing a conversation history because it demonstrates recall across sessions.
3. **Third — The Workflow Connects Insight to Action (Track 1):**  
   Demonstrates the containment operation and its verifiable state change, being precise that it updates Scout's application and graph-backed security data.

---

## 🔬 3. Four Technical Details Verified in Codebase

1. **Benchmark Consistency:**  
   Single authoritative empirical dataset from `scripts/benchmark.py` (measured on local FalkorDB engine over 100 iterations):
   - **Single-Node Indexed Lookup:** `0.37 ms` avg | `0.53 ms` p95 | `2,717 ops/s`
   - **3-Hop Blast Radius Traversal:** `1.69 ms` avg | `2.83 ms` p95 | `590 ops/s`
   - **Multi-Hop Credential & Access Path Audit:** `1.33 ms` avg | `2.32 ms` p95 | `750 ops/s`
   - **Episodic Procedural Memory Recall:** `1.43 ms` avg | `2.53 ms` p95 | `701 ops/s`
   - **End-to-End Multi-Hop Triage & Containment:** `7.21 ms` avg | `12.53 ms` p95 | `139 ops/s`
2. **Memory Terminology:**  
   Accurately defined as graph-based concept indexing and relationship recall across sessions in FalkorDB without overclaiming vector embedding similarity.
3. **Relationship Direction Consistency:**  
   Schema consistency verified: `(:Incident)-[:TRIGGERED_BY]->(:Log)` matches code (`db.create_edge("Incident", ..., "TRIGGERED_BY", "Log", ...)`), Cypher queries, and documentation diagrams.
4. **Evidence & Containment Verification:**  
   Cryptographic verification confirmed via `EvidenceExporter.verify_bundle()` SHA-256 integrity check and unit tested in `tests/test_scout.py`. Containment updates graph and runtime state with immutable audit trail.

---

## 🎥 4. Recording Strategy & Pro Tips

* **Live UI First:** Keep the live application visible for most of the video.
* **Subtle Zooms & Cuts:** Use brief zooms or cuts to emphasize the graph relationships, the new session ID, and the containment state change.
* **Concise Labels:** Add the small on-screen text labels at the beginning of each scene.
* **Pacing:** Let animations and voice alerts finish cleanly before moving to the next click.
* **The Climax Moment:** Scene 4 (fresh-session memory retrieval) is your strongest differentiator. Pause briefly on the returned incident card so judges clearly see the new session ID and historical context.
