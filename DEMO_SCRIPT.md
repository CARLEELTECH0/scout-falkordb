# 🎬 SCOUT: Optimized 3-Minute Video Demo & Walkthrough Guide

> **Target Duration:** 3:00 Minutes (180 seconds)  
> **Hackathon:** WeMakeDevs & FalkorDB Graph Hacks 2026  
> **Tracks Entered:**  
> 1. **Track 1:** Graph-Powered Action Agent  
> 2. **Track 2:** Agent Memory & Cross-Session Learning  
> 3. **Track 3:** The Company Brain  
> **Target Audience:** Technical Judges & Security Engineers  

---

## ⏱️ 1. The Three-Minute Judging Strategy

```
[0:00 - 0:15] The Hook: Show the Threat (15s)
              Capture attention immediately by triggering Attack Surge. 
              Show the graph changing before explaining Scout.

[0:15 - 0:50] Track 3: The Company Brain (35s)
              Trace the affected asset to its owner, supervisor, credentials, 
              and connected projects using a real FalkorDB Cypher query.

[0:50 - 1:35] Track 1: Graph-Powered Action Agent (45s)
              Show risk assessment (125/100), trigger containment workflow, 
              and verify the updated state in FalkorDB and UI. Be transparent 
              that this updates application and graph state rather than 
              physically isolating a production server.

[1:35 - 2:15] Track 2: Agent Memory (40s)
              Retrieve a previous incident in a fresh session. Show the stored 
              information and explain how it informs the new investigation.

[2:15 - 3:00] Evidence and Closing (45s)
              Export a real incident report, show actual test results (9 passing), 
              and finish with the specific value FalkorDB adds to Scout.
```

---

## 🎙️ 2. Optimized Three-Minute Narration & Screen Choreography

### 0:00 – 0:15 | The Hook
* **Screen View:** Full screen of Scout's Honeycomb graph at `http://localhost:8000`.
* **Action:** Immediately click **`⚡ Attack Surge`**. Watch the red threat pulse appear around `prod-auth-gateway`.
* **Spoken Narration:**
  > *"One compromised credential can expose an entire enterprise. The challenge isn't just detecting a threat — it's understanding what that threat connects to, remembering what happened before, and deciding what to do next.*  
  > *Meet **Scout**, an AI-powered enterprise investigator built with **FalkorDB**."*

---

### 0:15 – 0:50 | Track 3 — The Company Brain
* **Screen View:** Center Honeycomb Canvas & Left Inspector Ledger.
* **Action:**
  1. Click on node `AST-01` (`prod-auth-gateway`).
  2. The Inspector Ledger slides out on the left.
  3. Point the mouse to the lineage breadcrumbs (`Bob Martinez ➔ tok_98a ➔ prod-auth-gateway`) and the Cypher query block.
* **Spoken Narration:**
  > *"Here is **Track 3: The Company Brain**.*  
  > *Scout represents enterprise knowledge as a connected graph — employees, supervisors, infrastructure, credentials, and project dependencies.*  
  > *Instead of treating every record as an isolated piece of information, Scout follows the relationships to investigate the affected asset and identify its connected entities.*  
  > *FalkorDB powers these traversals using Cypher. Here, you can see the actual query, the resulting relationships, and the measured execution time of just 1.5 milliseconds."*

---

### 0:50 – 1:35 | Track 1 — Graph-Powered Action Agent
* **Screen View:** Left Inspector Ledger & Honeycomb Canvas.
* **Action:**
  1. Highlight the Risk Score (`125/100 CRITICAL`) and the 2 exposed staff members.
  2. Click **`🛡️ Quarantine Asset & Contain Breach`**.
  3. Pause for the built-in tactical voice alert: *"Threat contained. Target asset isolated in quarantine zone."*
  4. Watch the asset turn emerald green (`🟢 CONTAINED`) and the containment cell sprout into the graph.
* **Spoken Narration:**
  > *"Now, **Track 1: The Graph-Powered Action Agent**.*  
  > *I'll trigger a simulated security incident. Scout highlights the threat, evaluates the connected assets, and presents the risk assessment.*  
  > *After I authorize containment, Scout updates the incident state in the application and FalkorDB. Watch the affected asset change state, and listen to the confirmation.*  
  > *This demonstrates a graph-informed incident response workflow — from identifying relationships to executing and recording a containment action."*

---

### 1:35 – 2:15 | Track 2 — Agent Memory & Cross-Session Learning
* **Screen View:** Right Panel AI Narrative (`#narrative-col`).
* **Action:**
  1. Click **`💬 AI Narrative`** in the top bar (or the floating AI button).
  2. In the quick action suggestion chips, click **`🧠 Retrieve Memory (Fresh Session)`** (or type `"recall previous incident"` into the prompt bar).
  3. Watch the fresh session ID (`SES-XXXXXX`) generate and the rich FalkorDB memory card render live.
  4. Listen to the voice alert confirming retrieval of prior incident `INC-2026-001` and the `FirewallQuarantine` playbook.
* **Spoken Narration:**
  > *"Next, **Track 2: Agent Memory**.*  
  > *An investigation shouldn't lose its context when a session ends. Scout stores incident memories in FalkorDB and can retrieve them in a new session.*  
  > *Here, I'm retrieving a previous incident and its relevant context. That gives Scout a basis for connecting current investigations with earlier events.*  
  > *The goal is to make agent memory persistent and useful, rather than starting every investigation from zero."*

---

### 2:15 – 3:00 | Evidence and Closing
* **Screen View:** Top Bar `💾 Export Incident` ➔ Terminal running tests.
* **Action:**
  1. Click **`💾 Export Incident`** (or `Export Evidence Bundle (.md)`) to show the real forensic report download.
  2. Switch to terminal: show `python3 -m pytest tests/test_scout.py` passing **9/9 tests in 0.4s**.
  3. Show the 1-click `docker compose up` command in the README.
* **Spoken Narration:**
  > *"Finally, Scout can export an incident report for review and auditing.*  
  > *The project also includes a containerized startup workflow and automated tests. Here are the actual test results and the evidence generated by the application.*  
  > *FalkorDB is central to Scout because the investigation depends on relationships — who owns an asset, which credentials connect to it, what else is affected, and which previous incidents are relevant.*  
  > *Scout brings enterprise knowledge, persistent agent memory, and graph-informed incident response into one demonstrable system.*  
  > *Thank you to WeMakeDevs and FalkorDB for Graph Hacks 2026."*

---

## 🎯 3. The Five Changes Most Likely to Improve Your Score

### Priority 1 — Make Every Track Independently Verifiable
Give each track a visible label, one clear action, and one piece of evidence. The judge should not have to infer why a feature satisfies the track.
* **Track 3 Evidence:** Real Cypher query, line-of-reporting breadcrumb HUD, and sub-2ms traversal timing.
* **Track 1 Evidence:** Critical blast radius calculation, containment state transition (`🔴 CRITICAL` ➔ `🟢 CONTAINED`), and graph isolation cell sprout.
* **Track 2 Evidence:** Fresh session initialized live (`SES-XXXXXX`), previous incident `INC-2026-001` retrieved from FalkorDB, and historical playbook applied.

### Priority 2 — Prove FalkorDB is Essential
Show the real Cypher query against the running database, the returned entities, and the timing measurement. Explain why relationships are central to the investigation.
* Show the Cypher code block directly in the Inspector Ledger:
  ```cypher
  MATCH (e:Employee)-[:OWNS_TOKEN]->(t:SecurityToken)-[:GRANTS_ACCESS_TO]->(a:Asset {id: 'AST-01'})
  OPTIONAL MATCH (e)-[:REPORTS_TO*1..3]->(sup:Employee)
  OPTIONAL MATCH (p:Project)-[:DEPENDS_ON]->(a)
  RETURN e, t, sup, p
  ```

### Priority 3 — Make Memory the Surprise Moment
Click **`🧠 Retrieve Memory (Fresh Session)`** in the Narrative panel.
* Live generation of a fresh session ID in FalkorDB.
* Instant retrieval of past concept `BruteForceSpike` and past interaction `INC-2026-001`.
* Procedural recall of previous mitigation tool (`FirewallQuarantine`) with 100% containment record.

### Priority 4 — Add a Defensible Benchmark
Do not claim an unverified "300x speedup" over SQL without a direct side-by-side benchmark run. Instead, report actual empirical FalkorDB timings measured under controlled conditions:
* **Single-Node Indexed Lookup:** `0.37ms avg`
* **3-Hop Blast Radius Traversal:** `1.46ms avg` (`2.53ms p95`)
* **Multi-Hop Credential & Access Path Audit:** `1.56ms avg`
* **Episodic Procedural Memory Recall:** `1.10ms avg`
* **End-to-End Autonomous Triage:** `11.78ms avg`

### Priority 5 — Edit for Evidence, Not Spectacle
Keep the audio alert, subtle node animation, and smooth mouse movements. Remove long loading periods, unnecessary scrolling, and extended terminal footage. Use short zoom-ins for the query, timing, and test output.

---

## 🔬 4. How to Benchmark Without Weakening Your Submission

You do not need to claim FalkorDB is universally faster than every database. You need to demonstrate why it is appropriate for Scout's graph-oriented workload:
1. **Use equivalent data:** Populate both implementations with the same entities, relationships, and properties.
2. **Use equivalent semantics:** Compare the same four-hop investigation and return the same information.
3. **Report honestly:** State measured latency (e.g., `1.46ms` for 3-hop traversal in local FalkorDB). Focus on the architectural fit of native graph storage and Cypher for organizational lineage and agent memory.

---

## ✅ 5. Final 10-Point Pre-Recording Checklist

- [ ] **1. Official Track Names Verified:** Confirmed Track 1 (*Graph-Powered Action Agent*), Track 2 (*Agent Memory & Cross-Session Learning*), Track 3 (*The Company Brain*).
- [ ] **2. Reset Scout & Prepare State:** Click `🔄 Reset` so the graph starts clean and stable.
- [ ] **3. Verify Graph Query & Timing:** Click `AST-01` and verify the lineage HUD and Cypher query display cleanly.
- [ ] **4. Verify Containment State Transition:** Verify clicking `🛡️ Quarantine Asset` transitions `AST-01` from red to green and sprouts the containment cell.
- [ ] **5. Verify Persistent Memory Retrieval in Fresh Session:** Click `🧠 Retrieve Memory (Fresh Session)` and verify the fresh session ID and recalled incident card render.
- [ ] **6. Test Exported Incident Report:** Click `💾 Export Incident` and verify the download triggers.
- [ ] **7. Run Automated Tests:** Run `python3 -m pytest tests/test_scout.py` and confirm 9 passed in <0.5s.
- [ ] **8. Test Desktop Audio & Voice Alert:** Ensure browser audio is routed to your recording software so Scout's tactical voice synthesizer is clearly audible.
- [ ] **9. Check Resolution & Zoom:** Record at **1080p (1920x1080)**, browser zoom set to **110% or 125%** for crisp text.
- [ ] **10. Backup Recording:** Keep a backup raw take in case you want to do quick splices.
