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
* `MEMBER_OF`: Team affiliation
* `ASSIGNED_TO`: Project allocation
* `ACCESSED`: Infrastructure telemetry access
* `CONTAINS`: Project documentation provenance
* `AFFECTS`: Incident targeting infrastructure
* `TRIGGERED_BY`: Telemetry log generating security alert
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

### 2. Procedural & Semantic Memory Recall (Track 2)
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
