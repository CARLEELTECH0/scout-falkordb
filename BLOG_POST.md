# How We Built Scout: An Autonomous Enterprise Security & Knowledge Investigator on FalkorDB

> *Published for the **WeMakeDevs & FalkorDB Graph Hacks 2026** Hackathon*  
> *Target Tracks: Track 1 (Action Agent), Track 2 (Agent Memory), Track 3 (The Company Brain)*  
> *GitHub Repository: [github.com/CARLEELTECH0/scout-falkordb](https://github.com/CARLEELTECH0/scout-falkordb)*  

---

## 🚨 The 3:00 AM Alert: The Enterprise Data Silo Crisis

Imagine you are a security engineer on-call at 3:00 AM. A high-priority P1 alert fires: an anomalous volume of failed SSH root authentications is detected on `prod-auth-gateway`. 

To understand what is happening, you open four different tabs:
1. **Active Directory / Okta:** Who owns `tok_98a`? (Answer: Bob Martinez, Senior SecOps Engineer).
2. **Workday / Org Chart:** Who does Bob report to? Who is his team lead? (Alice Chen, Head of Infrastructure).
3. **AWS / Kubernetes Console:** What production databases and microservices live behind `prod-auth-gateway`? (Project FalconShield).
4. **Confluence / Notion:** What runbook or mitigation worked the last time we saw a credential-stuffing surge?

By the time you correlate the logs, identify the blast radius, and execute containment, **45 minutes have evaporated**. In a real breach, that is an eternity.

When data is trapped in relational tables and disconnected SaaS tools, investigating cross-cutting security incidents is painfully slow. We asked ourselves: **What if the entire enterprise—people, permissions, servers, incident logs, and autonomous agent memory—lived in a single, high-performance graph?**

Meet **Scout**.

---

## 💡 The Solution: Scout on FalkorDB

**Scout** is an autonomous enterprise knowledge and security investigator powered by **FalkorDB**. Instead of querying five separate databases, Scout represents the enterprise as a living, interconnected property graph.

By running on **FalkorDB's GraphBLAS matrix multiplication engine**, Scout traverses complex multi-hop relationships with **sub-millisecond latencies (<2ms)**. This speed allows autonomous AI agents to evaluate organizational blast radiuses, recall past incident playbooks, and contain threats in real-time.

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

Scout addresses all three hackathon tracks in one unified architecture.

---

## 🏢 Track 3: The Company Brain

Before an agent can make smart security decisions, it must understand organizational context. Scout models the entire enterprise hierarchy in FalkorDB:

* **People & Reporting Lines:** `(:Employee)-[:REPORTS_TO]->(:Employee)`
* **Team Allocations:** `(:Employee)-[:MEMBER_OF]->(:Team)`
* **Project Provenance:** `(:Project)-[:CONTAINS]->(:Document)`
* **Infrastructure Access:** `(:Employee)-[:OWNS_TOKEN]->(:SecurityToken)-[:GRANTS_ACCESS_TO]->(:Asset)`

### The 3-Hop Blast Radius Traversal
When asset `AST-01` (`prod-auth-gateway`) triggers an alert, Scout does not merely flag the machine. It executes a real-time Cypher traversal to map organizational exposure:

```cypher
MATCH (a:Asset {id: 'AST-01'})
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

In relational SQL, querying across employees, indirect managers, credentials, and projects requires multiple recursive CTEs and nested joins that degrade as tables grow. In FalkorDB, this 3-hop traversal completes in **1.69 milliseconds**.

Scout automatically scores the incident blast radius using a weighted formula:
$$\text{Risk Score} = (\text{Tier Weight} \times 25) + (\text{Staff Exposed} \times 15) + (\text{Projects Exposed} \times 20)$$

---

## 🎯 Track 1: The Graph-Powered Action Agent

Traditional security automation scripts rely on rigid, hardcoded if-else statements. Scout's `ScoutActionAgent` performs **autonomous multi-hop reasoning** over the graph.

### From Detection to Containment
1. **Telemetry Ingestion:** Scout ingests anomalous authentication telemetry from logs or our background threat simulator daemon.
2. **Graph Correlation:** It queries FalkorDB to associate the log with root-cause IP footprints and active credential tokens.
3. **Explainable Triage:** It generates an audit trail showing the reasoning hops:
   - *Hop 1:* Anomaly detected on `prod-auth-gateway`.
   - *Hop 2:* Traced to credential token `tok_98a` issued to Bob Martinez.
   - *Hop 3:* Cross-referenced against compliance rule SEC-402 (Zero-Trust Violation).
4. **State Containment Action:** The operator authorizes mitigation with one click. Scout triggers the containment protocol:
   - Updates `Asset.status` to `'Quarantined'` in FalkorDB.
   - Mutates graph edges by sprouting an immutable `(:QUARANTINED_BY)` audit relationship linked to the acting agent.
   - Speaks an instant tactical voice notification via the built-in browser speech engine: *"Threat contained. Asset prod-auth-gateway isolated in quarantine zone."*

---

## 🧠 Track 2: Agent Memory & Cross-Session Learning

One of the biggest flaws with LLM agents is amnesia: when an investigation session terminates, all learned context is lost.

In Scout, **agent memory is a first-class citizen inside FalkorDB**:
* **Episodic Sessions:** Every investigation session is saved as a `Session` node linked to the responsible agent.
* **Granular Interactions:** Prompts, responses, and reasoning verdicts are saved as `Interaction` nodes.
* **Graph-Based Concept Indexing:** Interactions link to security concepts like `BruteForceSpike` or `DataExfiltrationRisk` through `(:RECALLS)` relationships.

### The Fresh-Session Memory Reveal
When a new incident occurs, Scout does not start from zero. An agent initializes a **fresh session (`SES-XXXXXX`)** and queries FalkorDB for prior procedural memory:

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

Within **1.43 milliseconds**, FalkorDB returns:
- Historical incident: `INC-2026-001`.
- Past successful mitigation tool: `FirewallQuarantine`.
- Historical containment effectiveness: 100%.

The agent binds this historical knowledge into its fresh session, recommending an immediate, proven quarantine playbook.

---

## ⚡ Empirical Performance Benchmarks

To ensure our performance claims are grounded in reality, we built an automated benchmark harness (`scripts/benchmark.py`) that executes 100 iterations per workload against local FalkorDB:

| Operation / Cypher Workload | Avg Latency | p95 Latency | Throughput |
| :--- | :--- | :--- | :--- |
| **Single-Node Indexed Lookup (Employee)** | **0.37 ms** | 0.53 ms | **2,717 ops/s** |
| **3-Hop Blast Radius Traversal (Asset Exposure)** | **1.69 ms** | 2.83 ms | **590 ops/s** |
| **Multi-Hop Credential & Access Path Audit** | **1.33 ms** | 2.32 ms | **750 ops/s** |
| **Episodic Procedural Memory Recall** | **1.43 ms** | 2.53 ms | **701 ops/s** |
| **End-to-End Multi-Hop Triage & Containment** | **7.21 ms** | 12.53 ms | **139 ops/s** |

Every multi-hop graph query completes in **less than 2 milliseconds**—fast enough to support live, interactive visual dashboards and high-velocity autonomous agent loops.

---

## 🎨 Interactive User Experience: 3-Panel Side-by-Side Canvas

We engineered Scout's UI with a high-contrast palette of **burnt amber orange and obsidian black**:
1. **Left Panel — The Inspector Ledger:** Displays real-time telemetry footprints, blast radius risk meters, and the 1-click quarantine trigger.
2. **Center Canvas — Generative Honeycomb Visualizer:** Renders an interactive axial hexagonal grid with dynamic pulsing threat rings and real-time edge tracing.
3. **Right Panel — The AI Narrative Stream:** Features asynchronous agent collaboration between `Scout-Alpha` (Security Investigator) and `Policy-Beta` (Compliance Advisor), complete with animated audio equalizers and the **`🧠 Retrieve Memory (Fresh Session)`** action chip.

### Cryptographic Audit Bundles
Security compliance requires verifiable records. Scout features a 1-click evidence export endpoint (`/api/incidents/{id}/evidence`) that compiles a markdown post-mortem with a **cryptographic SHA-256 integrity checksum**. Anyone can verify the bundle's authenticity using `EvidenceExporter.verify_bundle()`.

---

## 🐳 1-Click Deployment (Docker Compose)

Scout is fully containerized. You can run FalkorDB and the entire Scout application locally with a single command:

```bash
git clone https://github.com/CARLEELTECH0/scout-falkordb.git
cd scout-falkordb
docker compose up
```

Open **`http://localhost:8000`** in your browser, and you have an enterprise graph security investigator running in seconds.

---

## 💡 What We Learned Building with FalkorDB

1. **Graph is the Natural Data Structure for Security:** Attackers think in graphs (lateral movement, credential paths). Defenders usually look at isolated log lists. Bringing enterprise data into FalkorDB levels the playing field.
2. **Sub-Millisecond Traversal Changes Agent Design:** When graph queries execute in 1–2 milliseconds, autonomous agents can perform exploratory multi-hop reasoning in real-time without introducing lag.
3. **Episodic Memory Belongs in the Graph:** Relational databases struggle with open-ended conversation associations. Modeling sessions, concepts, and interactions as graph nodes turns agent memory into a queryable, connected knowledge base.

---

## 🏁 Try Scout Today

* **GitHub Repository:** [https://github.com/CARLEELTECH0/scout-falkordb](https://github.com/CARLEELTECH0/scout-falkordb)
* **3-Minute Video Demo:** Included in repository documentation ([`DEMO_SCRIPT.md`](DEMO_SCRIPT.md))
* **Submission Write-up:** [`SUBMISSION.md`](SUBMISSION.md)

*Thank you to **WeMakeDevs** and **FalkorDB** for hosting Graph Hacks 2026!*
