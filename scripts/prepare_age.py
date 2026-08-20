import gzip
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET = BASE_DIR / "dataset" / "cit-HepPh.txt.gz"

NODES = BASE_DIR / "dataset" / "age_nodes.csv"
EDGES = BASE_DIR / "dataset" / "age_edges.csv"

nodes = set()

print("Reading dataset...")

with gzip.open(DATASET, "rt") as f:
    for line in f:
        if not line.strip() or line.startswith("#"):
            continue

        source, target = map(int, line.split())
        nodes.add(source)
        nodes.add(target)

print(f"Unique nodes: {len(nodes):,}")

with open(NODES, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "paper_id"])

    for node_id in sorted(nodes):
        writer.writerow([node_id, node_id])

print("Nodes CSV created.")

with gzip.open(DATASET, "rt") as src, open(EDGES, "w", newline="") as dst:
    writer = csv.writer(dst)

    writer.writerow([
        "start_id",
        "start_vertex_type",
        "end_id",
        "end_vertex_type"
    ])

    count = 0

    for line in src:
        if not line.strip() or line.startswith("#"):
            continue

        source, target = map(int, line.split())

        writer.writerow([
            source,
            "Paper",
            target,
            "Paper"
        ])

        count += 1

print(f"Edges CSV created: {count:,}")
print("AGE CSV preparation complete.")