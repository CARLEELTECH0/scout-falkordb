# ⚡ Scout: Core Cypher Queries & Graph Algorithm Catalog

This document details the primary Cypher queries and graph algorithms powering **Scout** across all three hackathon tracks.

---

## 🧠 Track 3: Company Brain Queries

### 1. Multi-Hop Organizational Blast Radius
Evaluates the downstream organizational impact if a target infrastructure asset is compromised.
```cypher
MATCH (a:Asset {id: $id})
OPTIONAL MATCH (inc:Incident)-[:AFFECTS]->(a)
OPTIONAL MATCH (e:Employee)-[:ACCESSED]->(a)
OPTIONAL MATCH (e)-[:ASSIGNED_TO]->(p:Project)
OPTIONAL MATCH (p)-[:CONTAINS]->(d:Document)
RETURN a.id AS asset_id,
       a.name AS asset_name,
       a.tier AS tier,
       a.type AS asset_type,
       collect(DISTINCT inc.id) AS related_incidents,
       collect(DISTINCT e.name) AS exposed_employees,
       collect(DISTINCT p.name) AS affected_projects,
       collect(DISTINCT d.title) AS exposed_documents
```
* **Algorithm Complexity:** O(k^d) where d=3 hops.
* **FalkorDB Optimization:** Utilizes vertex-centric indices on `(Asset.id)` and `(Project.id)`.

---

### 2. Employee Access Path Audit (Forensic Lineage)
Traces the shortest relationship path explaining how and why an employee reached an infrastructure asset.
```cypher
MATCH path = (e:Employee {id: $emp_id})-[*1..3]-(a:Asset {id: $asset_id})
RETURN [n in nodes(path) | {id: n.id, label: labels(n)[0], name: coalesce(n.name, n.title)}] AS nodes,
       [r in relationships(path) | type(r)] AS relationships
LIMIT 5
```

---

## 🤖 Track 2: Agent Memory & Coordination Queries

### 3. Episodic Conversation & Action Logging
Saves interaction nodes and binds them into persistent session subgraphs.
```cypher
MATCH (s:Session {id: $session_id})
CREATE (i:Interaction {
    id: $interaction_id,
    prompt: $prompt,
    response: $response,
    timestamp: $timestamp
})-[:RECORDED_IN]->(s)
WITH i
UNWIND $concepts AS concept_name
MERGE (c:Concept {id: 'CPT-' + toUpper(replace(concept_name, ' ', '_'))})
ON CREATE SET c.name = concept_name
MERGE (i)-[:RECALLS]->(c)
```

---

### 4. Procedural Memory Retrieval
Retrieves historical tool choices and resolutions when past agents faced identical or similar attack vectors.
```cypher
MATCH (c:Concept)
WHERE toLower(c.name) = toLower($name)
MATCH (i:Interaction)-[:RECALLS]->(c)
MATCH (i)-[:RECORDED_IN]->(s:Session)<-[:HAS_SESSION]-(a:Agent)
OPTIONAL MATCH (a)-[:USED_TOOL]->(t:Tool)
RETURN a.name AS agent_name,
       c.name AS concept,
       collect(DISTINCT t.name) AS tools_used,
       collect(DISTINCT i.response) AS past_solutions
```

---

### 5. Multi-Agent Task Delegation Handoff
Creates an audited handoff edge between collaborating specialized agents (e.g. Triage Agent -> Remediator Agent).
```cypher
MATCH (a1:Agent {id: $from_agent_id}), (a2:Agent {id: $to_agent_id})
CREATE (a1)-[:HANDED_OFF_TO {
    reason: $reason,
    incident_id: $incident_id,
