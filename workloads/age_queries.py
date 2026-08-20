def run_cypher(cur, query):
    sql = f"""
        SELECT *
        FROM ag_catalog.cypher(
            'cit_hepph'::name,
            $$
            {query}
            $$
        ) AS (result ag_catalog.agtype)
    """

    cur.execute(sql)
    return cur.fetchall()


def point_lookup(cur, node_id):
    return run_cypher(cur, f"""
        MATCH (p:Paper)
        WHERE p.paper_id =~ '{node_id}'
        RETURN p.paper_id
    """)


def traversal_1_hop(cur, node_id):
    return run_cypher(cur, f"""
        MATCH (p:Paper)
        WHERE p.paper_id =~ '{node_id}'
        MATCH (p)-[:CITES]->(q:Paper)
        RETURN q.paper_id
    """)


def traversal_2_hop(cur, node_id):
    return run_cypher(cur, f"""
        MATCH (p:Paper)
        WHERE p.paper_id =~ '{node_id}'
        MATCH (p)-[:CITES]->()-[:CITES]->(q:Paper)
        RETURN DISTINCT q.paper_id
    """)


def traversal_3_hop(cur, node_id):
    return run_cypher(cur, f"""
        MATCH (p:Paper)
        WHERE p.paper_id =~ '{node_id}'
        MATCH (p)-[:CITES]->()-[:CITES]->()-[:CITES]->(q:Paper)
        RETURN DISTINCT q.paper_id
    """)


def aggregation(cur):
    return run_cypher(cur, """
        MATCH (p:Paper)-[:CITES]->(q:Paper)
        RETURN count(*)
    """)