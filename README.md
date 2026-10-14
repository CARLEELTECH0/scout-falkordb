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

```
                  +----------------------------------------------+
                  |         Scout Interactive UI / Dashboard    |
                  |     (Live Vis.js Graph + Reasoning Stream)   |
                  +----------------------+-----------------------+
                                         |
                                         v
                         +---------------+---------------+
                         |   Scout FastAPI / MCP Server   |
                         +---------------+---------------+
                                         |
          +------------------------------+------------------------------+
          |                              |                              |
          v                              v                              v
+-------------------+          +-------------------+          +-------------------+
|  Company Brain    |          |   Agent Memory    |          |   Action Agent    |
|     (Track 3)     |          |     (Track 2)     |          |     (Track 1)     |
| - Blast Radius    |          | - Episodic Log    |          | - Multi-Hop Triage|
| - Access Auditing |          | - Semantic Recall |          | - Tool Selection  |
| - Org Context     |          | - Agent Handoff   |          | - Quarantine Exec |
+---------+---------+          +---------+---------+          +---------+---------+
          |                              |                              |
          +------------------------------+------------------------------+
                                         |
                                         v
                  +----------------------------------------------+
                  |              FalkorDB Engine                 |
                  |  - Embedded Zero-Config (falkordblite) OR    |
                  |  - Managed FalkorDB Cloud Instance           |
                  +----------------------------------------------+
```

---

## 📊 Unified Graph Schema

The database schema connects all three domains in a single, high-performance FalkorDB graph:

```
[Employee] ──(:REPORTS_TO)──> [Employee]
   │
   ├──(:MEMBER_OF)───> [Team]
   ├──(:ASSIGNED_TO)─> [Project] ──(:CONTAINS)──> [Document]
   └──(:ACCESSED)────> [Asset] <──(:AFFECTS)── [Incident] <──(:TRIGGERED_BY)── [Log]
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
