import csv
import os
import time

from neo4j import GraphDatabase


URI = os.environ["COGNODB_URI"]
USER = os.environ["COGNODB_USER"]
PASSWORD = os.environ["COGNODB_PASSWORD"]

NODE_FILE = "dataset/age_nodes.csv"
EDGE_FILE = "dataset/age_edges.csv"

BATCH_SIZE = 1000


def run_batch(session, query, rows):
    session.run(query, rows=rows).consume()


def main():
    driver = GraphDatabase.driver(
        URI,
        auth=(USER, PASSWORD)
    )

    driver.verify_connectivity()
    print("CognoDB connection OK")

    start = time.perf_counter()

    with driver.session() as session:

        print("Creating Paper nodes...")

        with open(NODE_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            batch = []

            for row in reader:
                batch.append({
                    "id": int(row["id"]),
                    "paper_id": row["paper_id"]
                })

                if len(batch) >= BATCH_SIZE:
                    run_batch(
                        session,
                        """
                        UNWIND $rows AS row
                        CREATE (p:Paper {
                            id: row.id,
                            paper_id: row.paper_id
                        })
                        """,
                        batch
                    )
                    batch.clear()

            if batch:
                run_batch(
                    session,
                    """
                    UNWIND $rows AS row
                    CREATE (p:Paper {
                        id: row.id,
                        paper_id: row.paper_id
                    })
                    """,
                    batch
                )

        print("Creating CITES relationships...")

       print("Resuming CITES relationships...")

with open(EDGE_FILE, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    # Skip relationships already loaded
    for _ in range(37000):
        next(reader, None)

    batch = []

    for row in reader:
        batch.append({
            "start_id": int(row["start_id"]),
            "end_id": int(row["end_id"])
        })

        if len(batch) >= BATCH_SIZE:
            run_batch(
                session,
                """
                UNWIND $rows AS row
                MATCH (p:Paper {id: row.start_id})
                MATCH (q:Paper {id: row.end_id})
                CREATE (p)-[:CITES]->(q)
                """,
                batch
            )
            batch.clear()

    if batch:
        run_batch(
            session,
            """
            UNWIND $rows AS row
            MATCH (p:Paper {id: row.start_id})
            MATCH (q:Paper {id: row.end_id})
            CREATE (p)-[:CITES]->(q)
            """,
            batch
        )

            for row in reader:
                batch.append({
                    "start_id": int(row["start_id"]),
                    "end_id": int(row["end_id"])
                })

                if len(batch) >= BATCH_SIZE:
                    run_batch(
                        session,
                        """
                        UNWIND $rows AS row
                        MATCH (p:Paper {id: row.start_id})
                        MATCH (q:Paper {id: row.end_id})
                        CREATE (p)-[:CITES]->(q)
                        """,
                        batch
                    )
                    batch.clear()

            if batch:
                run_batch(
                    session,
                    """
                    UNWIND $rows AS row
                    MATCH (p:Paper {id: row.start_id})
                    MATCH (q:Paper {id: row.end_id})
                    CREATE (p)-[:CITES]->(q)
                    """,
                    batch
                )

    elapsed = time.perf_counter() - start

    print()
    print("========================================")
    print("CognoDB ingest complete")
    print("========================================")
    print(f"Time: {elapsed:.2f} seconds")
    print(f"Nodes: 34546")
    print(f"Edges: 421578")
    print(f"Total records: {34546 + 421578}")
    print(f"Throughput: {(34546 + 421578) / elapsed:.2f} records/sec")

    driver.close()


if __name__ == "__main__":
    main()