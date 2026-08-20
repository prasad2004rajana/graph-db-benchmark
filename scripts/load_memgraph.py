import gzip
import sys
from pathlib import Path

from neo4j import GraphDatabase


BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "dataset" / "cit-HepPh.txt.gz"

URI = "bolt://localhost:7687"
USERNAME = ""
PASSWORD = ""

BATCH_SIZE = 5000


def load_dataset():
    driver = GraphDatabase.driver(
        URI,
        auth=(USERNAME, PASSWORD)
    )

    try:
        driver.verify_connectivity()
        print("Connected to Memgraph.")

        with driver.session() as session:
            batch = []
            total = 0

            with gzip.open(DATASET_PATH, "rt") as file:
                for line in file:

                    if not line.strip() or line.startswith("#"):
                        continue

                    source, target = map(int, line.split())
                    batch.append({
                        "source": source,
                        "target": target
                    })

                    if len(batch) >= BATCH_SIZE:
                        session.run(
                            """
                            UNWIND $edges AS edge
                            MERGE (a:Paper {id: edge.source})
                            MERGE (b:Paper {id: edge.target})
                            MERGE (a)-[:CITES]->(b)
                            """,
                            edges=batch
                        )

                        total += len(batch)
                        print(f"Loaded {total:,} relationships...")
                        batch.clear()

                if batch:
                    session.run(
                        """
                        UNWIND $edges AS edge
                        MERGE (a:Paper {id: edge.source})
                        MERGE (b:Paper {id: edge.target})
                        MERGE (a)-[:CITES]->(b)
                        """,
                        edges=batch
                    )

                    total += len(batch)

            print(f"Finished loading {total:,} relationships.")

    finally:
        driver.close()


if __name__ == "__main__":
    load_dataset()