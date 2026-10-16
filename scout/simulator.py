"""
Scout Security Threat & Attack Scenario Simulator
Generates realistic multi-vector security telemetry scenarios against FalkorDB infrastructure assets,
triggering live graph mutations, threat pulses, and automated agent triage.
"""

import random
import time
from typing import Dict, Any, Optional, List
from scout.db import FalkorGraph
from scout.agent import ScoutActionAgent

ATTACK_SCENARIOS = [
    {
        "vector": "AUTH_BRUTE_FORCE",
        "title": "Gateway Credential Brute-Force Surge",
        "target_asset_id": "AST-01",
        "level": "CRITICAL",
        "message": "AuthGateway Alert: 48 failed root and admin SSH authentication attempts from IP 192.168.1.105 within 1200ms",
        "recommended_concept": "BruteForceSpike"
    },
    {
        "vector": "BULK_DATA_EXFILTRATION",
        "title": "Anomalous Database Bulk Egress Spike",
        "target_asset_id": "AST-02",
        "level": "CRITICAL",
        "message": "Telemetry Anomaly: 4.8 GB outbound egress detected on prod-falcon-cluster port 6379 to unverified host 203.0.113.42",
        "recommended_concept": "DataExfiltrationRisk"
    },
    {
        "vector": "PRIVILEGE_ESCALATION",
        "title": "K8s Container Breakout & Syscall Injection",
        "target_asset_id": "AST-03",
        "level": "CRITICAL",
        "message": "Kernel Telemetry: Unauthorized ptrace syscall and capability elevation attempt detected on k8s-worker-node-01",
        "recommended_concept": "ClusterHealth"
    },
    {
        "vector": "CREDENTIAL_STUFFING",
        "title": "Distributed Botnet Token Stuffing",
        "target_asset_id": "AST-01",
        "level": "HIGH",
        "message": "Gateway Telemetry: Distributed spike of 120 invalid JWT bearer token presentations across 18 unique source subnets",
        "recommended_concept": "BruteForceSpike"
    }
]

class AttackSimulator:
    def __init__(self, db: Optional[FalkorGraph] = None):
        self.db = db or FalkorGraph.get_instance()
        self.agent = ScoutActionAgent(db=self.db)

    def trigger_attack(self, vector: Optional[str] = None, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Trigger a synthetic attack against the FalkorDB enterprise graph.
        Ingests telemetry, creates incident and log nodes, runs multi-hop investigation,
        and isolates the compromised asset.
        """
        if vector:
            scenario = next((s for s in ATTACK_SCENARIOS if s["vector"].upper() == vector.upper()), None)
            if not scenario:
                scenario = random.choice(ATTACK_SCENARIOS)
        else:
            scenario = random.choice(ATTACK_SCENARIOS)

        # Ingest into Scout Agent (mutates FalkorDB and creates Incident + Log)
        triage_result = self.agent.ingest_and_triage_log(
            message=scenario["message"],
            level=scenario["level"],
            target_asset_id=scenario["target_asset_id"],
            session_id=session_id
        )

        return {
            "status": "Triggered",
            "vector": scenario["vector"],
            "title": scenario["title"],
            "target_asset_id": scenario["target_asset_id"],
            "level": scenario["level"],
            "message": scenario["message"],
            "triage_result": triage_result,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

    def list_scenarios(self) -> List[Dict[str, Any]]:
        """Return all available attack scenarios."""
        return ATTACK_SCENARIOS

    def run_daemon(self, interval_seconds: int = 15, max_iterations: Optional[int] = None):
        """Run continuous threat simulation loop generating background SOC events."""
        print("=" * 72)
        print("   SCOUT 24/7 SOC THREAT SIMULATION DAEMON")
        print(f"   Feeding multi-vector attacks into FalkorDB every {interval_seconds}s")
        print("=" * 72)

        count = 0
        try:
            while True:
                count += 1
                attack = self.trigger_attack()
                inv = attack.get("triage_result", {}).get("investigation", {})
                print(f"\n[PULSE #{count}] Vector: {attack['vector']} | Target: {attack['target_asset_id']}")
                print(f"  Alert: {attack['message'][:65]}...")
                print(f"  Incident Created: {attack.get('triage_result', {}).get('incident_created')}")
                print(f"  Triage Verdict: {inv.get('final_status')} via {inv.get('tools_used', ['telemetry scan'])}")

                if max_iterations and count >= max_iterations:
                    print(f"\n[✓] Completed {count} simulation iterations.")
                    break

                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            print(f"\n[!] SOC simulation daemon stopped by operator ({count} events generated).")

