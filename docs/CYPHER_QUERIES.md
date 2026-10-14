# Cypher Query Catalog: Scout Enterprise Graph

## Track 3: Company Brain Queries

### 1. Organizational Blast Radius
```cypher
MATCH (target:Asset {id: $asset_id})
OPTIONAL MATCH (emp:Employee)-[acc:ACCESSED]->(target)
OPTIONAL MATCH (emp)-[:MEMBER_OF]->(t:Team)
OPTIONAL MATCH (emp)-[:ASSIGNED_TO]->(p:Project)
RETURN target.name AS asset_name, target.tier AS tier,
       collect(DISTINCT emp.name) AS exposed_employees,
       collect(DISTINCT t.name) AS affected_teams,
       collect(DISTINCT p.name) AS compromised_projects
```
