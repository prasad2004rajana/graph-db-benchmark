import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import psycopg2
from neo4j import GraphDatabase

from benchmark.metrics import calculate_latency_metrics


RUNS_PER_WORKER = 20


# ---------------------------------------------------------
# Neo4j
# ---------------------------------------------------------

NEO4J_URI = "bolt://localhost:7688"


def neo4j_query(node_id):
    driver = GraphDatabase.driver(NEO4J_URI, auth=None)

    try:
        with driver.session() as session:
            start = time.perf_counter()

            result = session.run(
                """
                MATCH (p:Paper)-[:CITES]->(q)
                RETURN q.id AS paper_id, count(*) AS citations
                ORDER BY citations DESC
                LIMIT 10
                """
            )

            list(result)

            return (time.perf_counter() - start) * 1000

    finally:
        driver.close()


def neo4j_mixed_operation(node_id):
    driver = GraphDatabase.driver(NEO4J_URI, auth=None)

    try:
        with driver.session() as session:
            start = time.perf_counter()

            # Read
            result = session.run(
                """
                MATCH (p:Paper {id: $id})-[:CITES]->(q)
                RETURN q.id AS id
                LIMIT 10
                """,
                id=node_id
            )
            list(result)

            # Write
            session.run(
                """
                MATCH (p:Paper {id: $id})
                SET p.benchmark_touch = $value
                """,
                id=node_id,
                value=int(time.time() * 1000)
            )

            return (time.perf_counter() - start) * 1000

    finally:
        driver.close()


# ---------------------------------------------------------
# Memgraph
# ---------------------------------------------------------

MEMGRAPH_URI = "bolt://localhost:7687"


def memgraph_query(node_id):
    driver = GraphDatabase.driver(
        MEMGRAPH_URI,
        auth=("", "")
    )

    try:
        with driver.session() as session:
            start = time.perf_counter()

            result = session.run(
                """
                MATCH (p:Paper {id: $id})-[:CITES]->(q)
                RETURN q.id AS id
                """,
                id=node_id
            )

            list(result)

            return (time.perf_counter() - start) * 1000

    finally:
        driver.close()


def memgraph_mixed_operation(node_id):
    driver = GraphDatabase.driver(
        MEMGRAPH_URI,
        auth=("", "")
    )

    try:
        with driver.session() as session:
            start = time.perf_counter()

            # Read
            result = session.run(
                """
                MATCH (p:Paper {id: $id})-[:CITES]->(q)
                RETURN q.id AS id
                LIMIT 10
                """,
                id=node_id
            )
            list(result)

            # Write
            session.run(
                """
                MATCH (p:Paper {id: $id})
                SET p.benchmark_touch = $value
                """,
                id=node_id,
                value=int(time.time() * 1000)
            )

            return (time.perf_counter() - start) * 1000

    finally:
        driver.close()


# ---------------------------------------------------------
# Apache AGE
# ---------------------------------------------------------

def age_query(node_id):
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

            start = time.perf_counter()

            sql = f"""
                SELECT *
                FROM ag_catalog.cypher(
                    'cit_hepph'::name,
                    $$
                    MATCH (p:Paper)
                    WHERE p.paper_id =~ '{node_id}'
                    MATCH (p)-[:CITES]->(q:Paper)
                    RETURN q.paper_id
                    $$
                ) AS (result ag_catalog.agtype)
            """

            cur.execute(sql)
            cur.fetchall()

            return (time.perf_counter() - start) * 1000

    finally:
        conn.close()


def age_mixed_operation(node_id):
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

            start = time.perf_counter()

            # Read
            read_sql = f"""
                SELECT *
                FROM ag_catalog.cypher(
                    'cit_hepph'::name,
                    $$
                    MATCH (p:Paper)
                    WHERE p.paper_id =~ '{node_id}'
                    MATCH (p)-[:CITES]->(q:Paper)
                    RETURN q.paper_id
                    $$
                ) AS (result ag_catalog.agtype)
            """

            cur.execute(read_sql)
            cur.fetchall()

            # Write
            write_sql = f"""
                SELECT *
                FROM ag_catalog.cypher(
                    'cit_hepph'::name,
                    $$
                    MATCH (p:Paper)
                    WHERE p.paper_id =~ '{node_id}'
                    SET p.benchmark_touch = {int(time.time() * 1000)}
                    RETURN p.paper_id
                    $$
                ) AS (result ag_catalog.agtype)
            """

            cur.execute(write_sql)
            cur.fetchall()

            conn.commit()

            return (time.perf_counter() - start) * 1000

    finally:
        conn.close()


# ---------------------------------------------------------
# Generic concurrency benchmark
# ---------------------------------------------------------

def benchmark_concurrency(name, query_function, node_id, concurrency):

    latencies = []

    start_time = time.perf_counter()

    total_requests = concurrency * RUNS_PER_WORKER

    with ThreadPoolExecutor(max_workers=concurrency) as executor:

        futures = [
            executor.submit(query_function, node_id)
            for _ in range(total_requests)
        ]

        for future in as_completed(futures):
            latencies.append(future.result())

    total_time = time.perf_counter() - start_time

    metrics = calculate_latency_metrics(latencies)

    throughput = len(latencies) / total_time

    print(f"\n{name}")
    print(f"Concurrency: {concurrency}")
    print(f"Requests:    {len(latencies)}")
    print(f"P50:         {metrics['p50_ms']:.3f} ms")
    print(f"P95:         {metrics['p95_ms']:.3f} ms")
    print(f"Mean:        {metrics['mean_ms']:.3f} ms")
    print(f"Throughput:  {throughput:.2f} req/s")


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":

    node_id = 9506257

    concurrency_levels = [1, 5, 10, 25]

    databases = [
        ("Neo4j", neo4j_query),
        ("Memgraph", memgraph_query),
        ("Apache AGE", age_query),
    ]

    print("\n" + "=" * 60)
    print("READ-ONLY CONCURRENCY BENCHMARK")
    print("=" * 60)

    for database_name, query_function in databases:

        print("\n" + "=" * 50)
        print(database_name)
        print("=" * 50)

        for concurrency in concurrency_levels:

            benchmark_concurrency(
                database_name,
                query_function,
                node_id,
                concurrency
            )

    print("\n" + "=" * 60)
    print("MIXED READ/WRITE CONCURRENCY BENCHMARK")
    print("=" * 60)

    mixed_databases = [
        ("Neo4j Mixed", neo4j_mixed_operation),
        ("Memgraph Mixed", memgraph_mixed_operation),
        ("Apache AGE Mixed", age_mixed_operation),
    ]

    for database_name, operation in mixed_databases:

        print("\n" + "=" * 50)
        print(database_name)
        print("=" * 50)

        for concurrency in concurrency_levels:

            benchmark_concurrency(
                database_name,
                operation,
                node_id,
                concurrency
            )