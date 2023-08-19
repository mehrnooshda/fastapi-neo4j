from fastapi import APIRouter, HTTPException, status, BackgroundTasks

from app.utils.db import neo4j_driver
from app.utils.schema import Relationship, Node

router = APIRouter()

relationship_types = ['sum', 'subtract', 'divide', 'multiply', 'result']


# @router.post('/calculate/{node_id}', response_model=Node)
def calculate_and_store(node_id: int, background_tasks = BackgroundTasks):
    cypher = f"""
            MATCH path=(start:User node_id:{node_id})-[*]->(end:User) 
            WITH start, REDUCE(first = start.value, op in COLLECT(op: TYPE(LAST(RELATIONSHIPS(path))), last: end.value) |
            CASE op.op
            WHEN 'ADD' THEN 1.0 * first + op.last
            WHEN 'MULTI' THEN 1.0 * first * op.last
            WHEN 'DIV' THEN 1.0 * first / op.last
            ELSE -1
            END) AS result RETURN result

            """

    with neo4j_driver.session() as session:
        result1 = session.run(
            query=cypher,
            parameters={
                'node_id': node_id
            },
        )

