import csv
import os
import time
import kuzu

DB_PATH = "kuzu_db"
NODE_FILE = "dataset/age_nodes.csv"
EDGE_FILE = "dataset/age_edges.csv"
EDGE_COPY_FILE = "dataset/kuzu_edges.csv"

if not os.path.exists(EDGE_COPY_FILE):
    print("Preparing relationship CSV...")

    with open(EDGE_FILE, newline="", encoding="utf-8") as src:
        reader = csv.DictReader(src)

        with open(EDGE_COPY_FILE, "w", newline="", encoding="utf-8") as dst:
            writer = csv.writer(dst)
            writer.writerow(["start_id", "end_id"])

            for row in reader:
                writer.writerow([
                    row["start_id"],
                    row["end_id"]
                ])

print("Opening Kuzu...")

db = kuzu.Database(DB_PATH)
conn = kuzu.Connection(db)

conn.execute("""
CREATE NODE TABLE IF NOT EXISTS Paper(
    id INT64,
    paper_id INT64,
    PRIMARY KEY(id)
)
""")

conn.execute("""
CREATE REL TABLE IF NOT EXISTS CITES(
    FROM Paper TO Paper
)
""")

print("Loading Paper nodes...")

start = time.perf_counter()

conn.execute(
    f'COPY Paper FROM "{NODE_FILE}" (header=true)'
)

node_time = time.perf_counter() - start

print(f"Nodes loaded in {node_time:.2f} seconds")

print("Loading CITES relationships...")

start = time.perf_counter()

conn.execute(
    f'COPY CITES FROM "{EDGE_COPY_FILE}" (header=true)'
)

edge_time = time.perf_counter() - start

print(f"Edges loaded in {edge_time:.2f} seconds")

node_count = conn.execute(
    "MATCH (p:Paper) RETURN count(p)"
).get_next()[0]

edge_count = conn.execute(
    "MATCH ()-[r:CITES]->() RETURN count(r)"
).get_next()[0]

print()
print("================================")
print("Kuzu load complete")
print("================================")
print(f"Nodes: {node_count}")
print(f"Edges: {edge_count}")
print(f"Node load time: {node_time:.2f}s")
print(f"Edge load time: {edge_time:.2f}s")