# 🎬 SCOUT: 3-Minute Video Demo & Walkthrough Script

> **Target Duration:** 3:00 Minutes (180 seconds)  
> **Hackathon:** WeMakeDevs & FalkorDB Graph Hacks 2026  
> **Speaker Role:** Enterprise Security Architect & Lead Builder

---

## ⏱️ Video Timeline Breakdown

```
[0:00 - 0:30] The Hook & The Problem (30s)
[0:30 - 1:15] Track 3: The Company Brain & Dynamic Honeycomb (45s)
[1:15 - 2:00] Track 1: Action Agent Multi-Hop Threat Triage (45s)
[2:00 - 2:30] Track 2: Agent Memory & Multi-Agent Collaboration (30s)
[2:30 - 3:00] Audit Evidence Export, Benchmarks & Wrap-up (30s)
```

---

### Segment 1: The Hook & The Problem (0:00 – 0:30)
* **Screen View:** Start on terminal running `docker compose up` or showing the clean Scout GitHub repository. Then switch to browser at `http://localhost:8000`.
* **Action:** Pan across the Honeycomb hero canvas showing the deep orange and obsidian black visualizer.
* **Voiceover:**
  > *"When a security incident hits an enterprise, analysts face a data silo nightmare. Active directory is in one database, server logs in another, and project permissions in a third. Connecting the dots manually takes hours.*  
  > *Meet **Scout** — an autonomous enterprise knowledge and security investigator powered by **FalkorDB**.*  
  > *Scout unifies the organization, infrastructure, agent memory, and live telemetry into a single, sub-millisecond knowledge graph."*

---

### Segment 2: Track 3 — The Company Brain & Dynamic Honeycomb (0:30 – 1:15)
* **Screen View:** Center Honeycomb Canvas at `http://localhost:8000`.
* **Action:**
  1. Hover over employee nodes (purple) and infrastructure asset nodes (orange/red).
  2. Click on `AST-01` (`prod-auth-gateway`) to highlight its relational lineage path.
  3. Show the dynamic lineage HUD: `Bob Martinez ➔ tok_98a ➔ prod-auth-gateway`.
* **Voiceover:**
  > *"Here is **Track 3: The Company Brain**. Notice the mathematical honeycomb grid.*  
  > *Employees and teams are rendered in violet, while infrastructure and threats are encoded in primary operational colors.*  
  > *When I click on `prod-auth-gateway`, Scout instantly traverses FalkorDB's property graph to map the complete organizational lineage: who owns this asset, which team they report to, and what confidential projects are downstream.*  
  > *Thanks to FalkorDB, this 3-hop graph traversal happens in just 1.7 milliseconds."*

---

### Segment 3: Track 1 — Action Agent Multi-Hop Threat Triage (1:15 – 2:00)
* **Screen View:** Top Navbar and Left Inspector Ledger.
* **Action:**
  1. Click **`⚡ Attack Surge`** in the top navbar.
  2. Observe the threat rings pulse in red around `AST-01`.
  3. Watch the Left Inspector Ledger smoothly slide out side-by-side with the graph.
  4. Point out the live telemetry footprint, the Risk Score (`125/100 CRITICAL`), and the 4-hop Cypher breadcrumbs.
  5. Click **`🛡️ Quarantine Asset & Contain Breach`**.
  6. Listen to the tactical audio alert: *"Threat contained. Asset prod-auth-gateway isolated in quarantine zone."*
  7. Show the asset turn green and the containment cell sprout into the graph.
* **Voiceover:**
  > *"Now let's demonstrate **Track 1: The Graph-Powered Action Agent**.*  
  > *I'll trigger a live credential brute-force attack surge. Notice the red threat pulse rings.*  
  > *The Inspector Ledger pops out on the left: Scout has autonomously correlated the log telemetry, calculated a critical blast radius of 125, and flagged 2 exposed staff members.*  
  > *With one click, I authorize mitigation. Scout executes `TOOL-02 (FirewallQuarantine)`, updates the graph node in FalkorDB, and our built-in tactical voice engine confirms containment live."*

---

### Segment 4: Track 2 — Agent Memory & Cross-Session Learning (2:00 – 2:30)
* **Screen View:** Right Panel AI Team Narrative (`#narrative-col`).
* **Action:**
  1. Click **`💬 AI Narrative`** or the floating launcher button in the bottom right.
  2. Show all 3 panels sitting side-by-side without any overlap.
  3. Point to the dual-stream conversation between `Scout-Alpha` and `Policy-Beta`.
  4. Type a directive into the console: `"Audit active session tokens across all tier-1 assets"`.
  5. Watch both agents respond and the audio equalizer bars bounce.
* **Voiceover:**
  > *"In **Track 2: Agent Memory**, Scout maintains persistent episodic sessions and procedural recall in FalkorDB.*  
  > *On the right, we have the AI Narrative Stream. When threats occur, `Scout-Alpha` recalls historical playbooks stored under concept nodes like `BruteForceSpike`.*  
  > *If an escalation is required, tasks are transferred directly in the graph to `Scout-Beta` with a verified audit trail.*  
  > *And notice our seamless 3-panel layout: the Inspector Ledger, the Honeycomb Canvas, and the Narrative live side-by-side in real-time."*

---

### Segment 5: Evidence Export, Benchmarks & Wrap-Up (2:30 – 3:00)
* **Screen View:** Left Inspector Ledger -> Terminal running `scripts/benchmark.py`.
* **Action:**
  1. Click **`📥 Export Evidence Bundle (.md)`** in the Inspector Ledger to download the markdown file.
  2. Quick cut to the terminal running `python3 scripts/benchmark.py` showing **~3,000 ops/s** and sub-millisecond latencies.
  3. Close on the GitHub repository README.
* **Voiceover:**
  > *"For SOC 2 compliance, Scout provides 1-click export of an audit-ready incident post-mortem with a SHA-256 cryptographic checksum, graph provenance, and memory tags.*  
  > *In our benchmark suite, FalkorDB delivers single-node indexed lookups in 0.33 milliseconds and end-to-end multi-hop autonomous triage in just 6 milliseconds.*  
  > *You can run the entire system right now with a single `docker compose up`.*  
  > *Thank you, WeMakeDevs and FalkorDB!"*

---

## 💡 Quick Tips for Recording
* **Resolution:** 1080p (1920x1080) or 1440p at 60 FPS.
* **Audio:** Make sure browser audio is captured so the Web Speech tactical voice alerts are audible in the video.
* **Browser:** Chrome or Brave in full-screen (F11) with dark mode active.
