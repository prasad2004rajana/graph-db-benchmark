def point_lookup(session, node_id):
    result = session.run(
        """
        MATCH (p:Paper {id: $id})
        RETURN p.id AS id
        """,
        id=node_id
    )
    return result.single()


def traversal_1_hop(session, node_id):
    result = session.run(
        """
        MATCH (p:Paper {id: $id})-[:CITES]->(q)
        RETURN q.id AS id
        """,
        id=node_id
    )
    return list(result)


def traversal_2_hop(session, node_id):
    result = session.run(
        """
        MATCH (p:Paper {id: $id})-[:CITES]->()-[:CITES]->(q)
        RETURN DISTINCT q.id AS id
        """,
        id=node_id
    )
    return list(result)


def traversal_3_hop(session, node_id):
    result = session.run(
        """
        MATCH (p:Paper {id: $id})
              -[:CITES]->()
              -[:CITES]->()
              -[:CITES]->(q)
        RETURN DISTINCT q.id AS id
        """,
        id=node_id
    )
    return list(result)


def aggregation(session):
    result = session.run(
        """
        MATCH (p:Paper)-[:CITES]->(q)
        RETURN q.id AS paper_id, count(*) AS citations
        ORDER BY citations DESC
        LIMIT 10
        """
    )
    return list(result)

def filtered_lookup(session, node_id):
    result = session.run(
        """
        MATCH (p:Paper)
        WHERE p.id = $id
        RETURN p.id AS id, p.paper_id AS paper_id
        """,
        id=node_id
    )
    return list(result)