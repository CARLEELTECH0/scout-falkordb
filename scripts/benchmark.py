#!/usr/bin/env python3
"""
Scout & FalkorDB Performance Benchmark Suite
Measures sub-millisecond Cypher query throughput, multi-hop blast radius traversal speed,
and episodic memory recall latency against FalkorDB.
"""

import time
import statistics
from scout.db import FalkorGraph
from scout.brain import CompanyBrain
from scout.memory import AgentMemory
from scout.agent import ScoutActionAgent

def benchmark_operation(name: str, func, iterations: int = 100):
    latencies = []
    # Warmup
    for _ in range(5):
        func()

    start_total = time.perf_counter()
    for _ in range(iterations):
        t0 = time.perf_counter()
        func()
        t1 = time.perf_counter()
        latencies.append((t1 - t0) * 1000.0)  # ms
    total_time = time.perf_counter() - start_total

    avg_ms = statistics.mean(latencies)
    median_ms = statistics.median(latencies)
    p95_ms = statistics.quantiles(latencies, n=20)[18] if len(latencies) >= 20 else max(latencies)
    ops_per_sec = iterations / total_time

    return {
        "operation": name,
        "iterations": iterations,
        "avg_ms": avg_ms,
        "median_ms": median_ms,
        "p95_ms": p95_ms,
        "ops_sec": ops_per_sec
    }

def main():
    print("=" * 76)
    print("   SCOUT & FALKORDB HIGH-THROUGHPUT GRAPH BENCHMARK SUITE")
    print("   Target: FalkorDB Graph Engine (Local / Cloud)")
    print("=" * 76)

    db = FalkorGraph.get_instance()
    brain = CompanyBrain(db)
    memory = AgentMemory(db)
    agent = ScoutActionAgent(db=db)

    results = []

    # Benchmark 1: Single-Node Indexed Lookup
    results.append(benchmark_operation(
        "Single-Node Indexed Lookup (Employee)",
        lambda: db.query("MATCH (e:Employee {id: 'EMP-02'}) RETURN e.name"),
        iterations=100
    ))

    # Benchmark 2: 3-Hop Blast Radius Traversal (Company Brain)
    results.append(benchmark_operation(
        "3-Hop Blast Radius Traversal (Asset Exposure)",
        lambda: brain.compute_blast_radius("AST-01"),
        iterations=100
    ))

    # Benchmark 3: Multi-Hop Access Path Audit
    results.append(benchmark_operation(
        "Multi-Hop Credential & Access Path Audit",
        lambda: brain.audit_access_path("EMP-02", "AST-01"),
        iterations=100
    ))

    # Benchmark 4: Procedural Memory Concept Recall
    results.append(benchmark_operation(
        "Episodic Procedural Memory Recall (FalkorDB)",
        lambda: memory.recall_procedural_memory("BruteForceSpike"),
        iterations=100
    ))

    # Benchmark 5: End-to-End Autonomous Incident Triage
    results.append(benchmark_operation(
        "End-to-End Multi-Hop Triage & Containment",
        lambda: agent.investigate_incident("INC-2026-001"),
        iterations=50
    ))

    # Print Formatted Table
    print("\n" + "-" * 76)
    print(f"{'Operation / Cypher Workload':<42} | {'Avg (ms)':<9} | {'p95 (ms)':<9} | {'Throughput'}")
    print("-" * 76)
    for r in results:
        print(f"{r['operation']:<42} | {r['avg_ms']:>7.2f}ms | {r['p95_ms']:>7.2f}ms | {r['ops_sec']:>6.0f} ops/s")
    print("-" * 76)
    print("✓ FalkorDB Graph Traversal & Autonomous Agent benchmarks completed successfully.\n")

if __name__ == "__main__":
    main()
