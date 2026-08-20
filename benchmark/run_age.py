import sys
import time

import psycopg2

from workloads.age_queries import (
    point_lookup,
    filtered_lookup,
    traversal_1_hop,
    traversal_2_hop,
    traversal_3_hop,
    aggregation,
)

from benchmark.metrics import calculate_latency_metrics


WARMUP_RUNS = 10
MEASURED_RUNS = 100


def benchmark(name, operation):
    print(f"\nRunning: {name}")

    for _ in range(WARMUP_RUNS):
        operation()

    latencies = []

    for _ in range(MEASURED_RUNS):
        start = time.perf_counter()

        operation()

        elapsed = (time.perf_counter() - start) * 1000
        latencies.append(elapsed)

    metrics = calculate_latency_metrics(latencies)

    print(f"  P50 : {metrics['p50_ms']:.3f} ms")
    print(f"  P95 : {metrics['p95_ms']:.3f} ms")
    print(f"  Mean: {metrics['mean_ms']:.3f} ms")

    return metrics


def main(node_id):
    conn = psycopg2.connect(
        host="localhost",
        port=5433,
        database="postgres",
        user="postgres",
        password="benchmark"
    )

    try:
        with conn.cursor() as cur:

            cur.execute("LOAD 'age'")
            cur.execute(
                "SET search_path TO ag_catalog, '$user', public"
            )

            benchmark(
                "Point Lookup",
                lambda: point_lookup(cur, node_id)
            )

            benchmark(
                "Filtered Lookup",
                lambda: filtered_lookup(cur, node_id)
            )

            benchmark(
                "1-Hop Traversal",
                lambda: traversal_1_hop(cur, node_id)
            )

            benchmark(
                "2-Hop Traversal",
                lambda: traversal_2_hop(cur, node_id)
            )

            benchmark(
                "3-Hop Traversal",
                lambda: traversal_3_hop(cur, node_id)
            )

            benchmark(
                "Aggregation",
                lambda: aggregation(cur)
            )

    finally:
        conn.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python benchmark/run_age.py <node_id>")
        sys.exit(1)

    main(int(sys.argv[1]))
