import time
import kuzu

DB_PATH = "kuzu_db"
NODE_ID = 9506257
RUNS = 100
WARMUP = 10


db = kuzu.Database(DB_PATH)
conn = kuzu.Connection(db)


def benchmark(name, query):
    for _ in range(WARMUP):
        conn.execute(query)

    times = []

    for _ in range(RUNS):
        start = time.perf_counter()
        result = conn.execute(query)

        while result.has_next():
            result.get_next()

        times.append((time.perf_counter() - start) * 1000)

    times.sort()

    p50 = times[int(len(times) * 0.50)]
    p95 = times[int(len(times) * 0.95)]
    mean = sum(times) / len(times)

    print(f"\n{name}")
    print(f"P50 : {p50:.3f} ms")
    print(f"P95 : {p95:.3f} ms")
    print(f"Mean: {mean:.3f} ms")


benchmark(
    "Point Lookup",
    f"""
    MATCH (p:Paper)
    WHERE p.id = {NODE_ID}
    RETURN p.id
    """
)
benchmark(
    "Filtered Lookup",
    f"""
    MATCH (p:Paper)
    WHERE p.id = {NODE_ID} AND p.id IS NOT NULL
    RETURN p.id
    """
)

benchmark(
    "1-Hop Traversal",
    f"""
    MATCH (p:Paper)-[:CITES]->(q:Paper)
    WHERE p.id = {NODE_ID}
    RETURN q.id
    """
)

benchmark(
    "2-Hop Traversal",
    f"""
    MATCH (p:Paper)-[:CITES]->()-[:CITES]->(q:Paper)
    WHERE p.id = {NODE_ID}
    RETURN DISTINCT q.id
    """
)

benchmark(
    "3-Hop Traversal",
    f"""
    MATCH (p:Paper)-[:CITES]->()-[:CITES]->()-[:CITES]->(q:Paper)
    WHERE p.id = {NODE_ID}
    RETURN DISTINCT q.id
    """
)

benchmark(
    "Aggregation",
    """
    MATCH (p:Paper)-[:CITES]->(q:Paper)
    RETURN q.id, count(*) AS citations
    ORDER BY citations DESC
    LIMIT 10
    """
)