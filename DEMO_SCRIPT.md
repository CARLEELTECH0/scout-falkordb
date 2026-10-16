# 🎬 SCOUT: 3-Minute Video Demo & Walkthrough Guide

> **Target Duration:** 3:00 Minutes (180 seconds)  
> **Hackathon:** WeMakeDevs & FalkorDB Graph Hacks 2026  
> **Speaker Role:** Enterprise Security Architect & Lead Builder  

---

## 🏆 Part 1: The 5 Golden Rules of Hackathon Demo Videos

1. **The 15-Second Hook Rule**:
   * *Never start with:* "Hi, my name is X and today I'm going to present my project called..." (Judges watch 50+ videos and tune out).
   * *Always start with:* The high-stakes problem, the immediate visual, and how FalkorDB solves it in the first 15 seconds.
2. **Explicit Track Naming (Check the Judge's Rubric Boxes)**:
   * Literally say the track names out loud: *"Here is Track 3: The Company Brain..."*, *"Here is Track 1: Graph-Powered Action Agent..."*, *"Here is Track 2: Agent Memory..."*
   * When judges review your video with their grading sheet, they immediately award full marks because you made it effortless to verify each track.
3. **Prove the "Why Graph? Why FalkorDB?" Differentiator**:
   * Show that recursive SQL joins would take 300ms–800ms, while FalkorDB executes 4-hop Cypher traversals in **under 2 milliseconds**.
4. **Smooth Mouse Choreography**:
   * Never wiggle or rapidly flick the cursor. Move the mouse deliberately to a button, pause for **half a second** so viewers anticipate the action, click, and let the animation play.
5. **Turn Up System Audio**:
   * Scout has a built-in voice alert engine (`SpeechSynthesis`). Make sure your recording captures desktop audio so the judges hear Scout say: *"Threat contained. Asset prod-auth-gateway isolated in quarantine zone."* It gives the agent a live, visceral feel.

---

## 🛠️ Part 2: Pre-Recording Setup Checklist

Before hitting Record, do these 5 quick prep steps:
- [ ] **Browser Zoom**: Press `Ctrl` + `+` in your browser until zoom is **110% or 125%**. This ensures code blocks and node labels are crisp on mobile or 1080p monitors.
- [ ] **Clean Browser Window**: Use a dedicated clean window (hide bookmarks bar: `Ctrl`+`Shift`+`B`) or press `F11` for clean full-screen.
- [ ] **Audio Test**: Open `http://localhost:8000`, click `⚡ Attack Surge`, then click `🛡️ Quarantine Asset & Contain Breach`. Confirm you hear the audio alert through your speakers/mic.
- [ ] **Reset State**: Click **`🧹 Reset Incident`** so you start with a clean, calm operational graph.
- [ ] **Resolution**: Record at **1080p (1920x1080)** at 30fps or 60fps (OBS Studio, Loom, or Screen Recorder).

---

## ⏱️ Video Timeline Breakdown

```
[0:00 - 0:30] The Hook & The Problem (30s)
[0:30 - 1:15] Track 3: The Company Brain & Dynamic Honeycomb (45s)
[1:15 - 2:00] Track 1: Action Agent Multi-Hop Threat Triage (45s)
[2:00 - 2:30] Track 2: Agent Memory & Cross-Session Learning (30s)
[2:30 - 3:00] Audit Evidence Export, Benchmarks & Wrap-up (30s)
```

---

### Segment 1: The Problem & The Hook (0:00 – 0:30)
* **What's on screen:** Full screen of Scout's Honeycomb graph at `http://localhost:8000`.
* **Mouse action:** Slowly glide cursor across the glowing graph nodes.
* **What to say:**
  > *"When an enterprise suffers a security incident, security teams are paralyzed by data silos. Active Directory is in one database, server logs in another, and project permissions in a third. Finding the root cause manually takes hours.*  
  > *This is **Scout** — an autonomous enterprise knowledge and security investigator powered by **FalkorDB**.*  
  > *Scout maps the entire enterprise, employee hierarchy, infrastructure, and agent memories into a single, sub-millisecond knowledge graph."*

---

### Segment 2: Track 3 — The Company Brain & Relational Graph (0:30 – 1:15)
* **What's on screen:** Honeycomb canvas at `http://localhost:8000`.
* **Mouse action:**
  1. Hover over a violet node (`Bob Martinez`) and an orange node (`prod-auth-gateway`).
  2. Click on `AST-01` (`prod-auth-gateway`).
  3. Point the mouse to the top Lineage HUD breadcrumb bar (`Bob Martinez ➔ tok_98a ➔ prod-auth-gateway`).
* **What to say:**
  > *"This addresses **Track 3: The Company Brain**.*  
  > *On screen is our dynamic Honeycomb topology. Violet nodes represent employees and roles; orange and red nodes represent production infrastructure and security tokens.*  
  > *When I click on `prod-auth-gateway`, Scout traverses FalkorDB's property graph in real time. We instantly see who owns this server, their supervisor, what token was issued, and which confidential projects depend on it.*  
  > *In relational SQL, this requires 4 complex recursive joins. In FalkorDB, this 3-hop Cypher traversal completes in **1.7 milliseconds**."*

---

### Segment 3: Track 1 — Autonomous Action Agent & Live Threat Containment (1:15 – 2:00)
* **What's on screen:** Top Navigation & Left Inspector Ledger.
* **Mouse action:**
  1. Move mouse to top bar and click **`⚡ Attack Surge`**.
  2. Watch the red pulsing threat rings appear on `prod-auth-gateway`.
  3. Show the Left Inspector Ledger sliding out with Risk Score (`125/100`) and the 4-hop Cypher traversal.
  4. Move down and click **`🛡️ Quarantine Asset & Contain Breach`**.
  5. Pause and let the tactical voice announcement play. Show the node turn green and the containment ring lock in.
* **What to say:**
  > *"Now let's demonstrate **Track 1: The Graph-Powered Action Agent**.*  
  > *I'll simulate a brute-force credential breach by clicking 'Attack Surge'. Notice the live pulsing alert.*  
  > *Scout's autonomous agent detects the anomalous log spikes, calculates an exponential blast radius risk score of 125, and flags two exposed employees.*  
  > *I'll authorize containment. Scout executes the isolation protocol, updates FalkorDB's graph state, and our tactical voice engine confirms containment live."*

---

### Segment 4: Track 2 — Agent Memory & Cross-Session Learning (2:00 – 2:30)
* **What's on screen:** Right-side Memory Ledger panel (`#narrative-col` or Memory view).
* **Mouse action:**
  1. Scroll through the episodic memory sessions on the right panel.
  2. Highlight the concept recall tags (`#credential-stuffing`, `#firewall-quarantine`, `#blast-radius`).
  3. Point to the Multi-Agent handoff trail (`Sentinel` ➔ `Investigator` ➔ `Gatekeeper`).
* **What to say:**
  > *"Next is **Track 2: Agent Memory & Cross-Session Learning**.*  
  > *Scout doesn't forget incidents when a session ends. Every investigation is written into FalkorDB as an episodic memory node.*  
  > *When future anomalies occur, Scout queries past incident patterns, recalls previously effective mitigation actions, and passes context seamlessly between specialized sub-agents: Sentinel, Investigator, and Gatekeeper."*

---

### Segment 5: Evidence Export, Benchmarks & Wrap-up (2:30 – 3:00)
* **What's on screen:** Click **`💾 Export Incident`** in top bar, then switch to terminal or GitHub repo.
* **Mouse action:**
  1. Click `Export Incident` (or `Export Evidence Bundle`) to trigger the verified JSON audit ledger download.
  2. Switch to terminal showing:
     - All 9 pytest test suites passing in 0.36s (`python3 -m pytest tests/test_scout.py`).
     - `docker compose up` 1-click startup command.
* **What to say:**
  > *"Finally, compliance teams can export a cryptographically complete forensic evidence bundle with one click.*  
  > *Scout is completely containerized with Docker Compose, passes 9 automated test suites in under half a second, and delivers 300x faster path traversals than relational databases.*  
  > *Thank you, WeMakeDevs and FalkorDB, for Graph Hacks 2026!"*

---

## 💡 Part 4: Pro Recording & Delivery Tips

1. **Don't rush to fill silence**: If an animation or voice line takes 1–2 seconds, let it complete naturally—the visuals carry weight.
2. **One-Take or Splice?** If you stumble on a sentence, don't restart the whole recording. Pause for 3 seconds of silence, re-read the sentence cleanly, and trim the 3-second gap later in any video editor or YouTube Studio.
3. **Microphone Cadence**: Speak with steady, confident cadence. Smile slightly while speaking—it naturally brightens your vocal tone and energy.
