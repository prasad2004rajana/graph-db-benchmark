import csv
import os
import time

from neo4j import GraphDatabase

URI = os.environ["COGNODB_URI"]
USER = os.environ["COGNODB_USER"]
PASSWORD = os.environ["COGNODB_PASSWORD"]

EDGE_FILE = "dataset/age_edges.csv"

# Already loaded successfully
SKIP_EDGES = 37000

# Smaller batches are safer for the free C0 instance
BATCH_SIZE = 250


def main():
    driver = GraphDatabase.driver(
        URI,
        auth=(USER, PASSWORD),
        max_connection_lifetime=300,
    )

    driver.verify_connectivity()
    print("CognoDB connection OK")

    start = time.perf_counter()
    loaded = 0

    with driver.session() as session:
        with open(EDGE_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for _ in range(SKIP_EDGES):
                next(reader, None)

            batch = []

            for row in reader:
                batch.append({
                    "start_id": int(row["start_id"]),
                    "end_id": int(row["end_id"]),
                })

                if len(batch) >= BATCH_SIZE:
                    session.run(
                        """
                        UNWIND $rows AS row
                        MATCH (p:Paper {id: row.start_id})
                        MATCH (q:Paper {id: row.end_id})
                        CREATE (p)-[:CITES]->(q)
                        """,
                        rows=batch,
                    ).consume()

                    loaded += len(batch)
                    batch.clear()

                    if loaded % 5000 == 0:
                        print(f"Additional edges loaded: {loaded}")

            if batch:
                session.run(
                    """
                    UNWIND $rows AS row
                    MATCH (p:Paper {id: row.start_id})
                    MATCH (q:Paper {id: row.end_id})
                    CREATE (p)-[:CITES]->(q)
                    """,
                    rows=batch,
                ).consume()

                loaded += len(batch)

    elapsed = time.perf_counter() - start

    print()
    print("========================================")
    print("CognoDB relationship resume complete")
    print("========================================")
    print(f"Additional edges: {loaded}")
    print(f"Time: {elapsed:.2f} seconds")
    print(f"Throughput: {loaded / elapsed:.2f} edges/sec")

    driver.close()


if __name__ == "__main__":
    main()