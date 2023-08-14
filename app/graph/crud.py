from fastapi import APIRouter, HTTPException, status

from app.utils.db import neo4j_driver
from app.utils.schema import Relationship, Node

router = APIRouter()

relationship_types = ['sum', 'subtract', 'divide', 'multiply', 'result']


@router.get('/node/{node_id}', response_model=Node) # todo: create when method is post (error handling)
def retrieve_node(node_id: int):
    cypher = """
    MATCH (node) 
    WHERE ID(node) = $node_id
    return ID(node) as id, LABEL(node) as label, node
    """

    with neo4j_driver.session() as session:
        result = session.run(query=cypher,
                             parameters={'node_id': node_id})

        if not result or result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Node not found.")

        node_data = result.data()[0]

    return Node(node_id=node_data['id'],
                labels=node_data['label'],
                properties=node_data['node'])
def write_data(res):
    record = res.single()
    value = record.value()
    info = res.consume()
    return value, info

@router.post('/create_node', response_model=Node)
def create_node(label: str, node_attributes: dict):
    print(node_attributes.items(), "node_attributes")
    unpacked_attributes = ', '.join(f'new_node.{key} = \'{value}\'' for (key, value) in node_attributes.items())
    print("unpacked_attributes", unpacked_attributes)
    cypher = f"""
            CREATE (new_node:{label})
            SET {unpacked_attributes}
            RETURN new_node,
             LABELS(new_node) as labels, ID(new_node) as id
            """

    with neo4j_driver.session() as session:
        result1 = session.run(
            query=cypher,
            parameters={
                'attributes': node_attributes
            },
        )
    # mmm = [dict(i) for i in result1]
    lll = list(result1)
    print('result1', lll)
    print('........', '\n')
    for record in result1:
        print('1')
        print(record)

        # Access data from the record using keys or indices
        # node_data = record.get("new_node")  # Assuming "new_node" is a key in your query result
        # labels = record.get("labels")
        # node_id = record.get("id")
        #
        # print("Node Data:", node_data)
        # print("Labels:", labels)
        # print("Node ID:", node_id)


    node_data = result1.data()[0]

    return Node(node_id=node_data['id'],
                label=node_data['label'],
                properties=node_data['new_node'])


@router.post('/create_relationship', response_model=Relationship)
def create_relationship(source_node_id, target_node_id, relationship_type):
    if relationship_type not in relationship_types:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Permission denied, relationship type is not acceptable",
            headers={"WWW-Authenticate": "Bearer"}
        )
    cypher = f"""
        MATCH (sourceNode:{source_node_id: $source_node_id}) 
        MATCH (targetNode:{target_node_id: $target_node_id}) 
        CREATE (sourceNode)-[relationship:{relationship_type}]->(targetNode)

        RETURN sourceNode, targetNode, ID(sourceNode), ID(targetNode), ID(relationship), TYPE(relationship) """
    with neo4j_driver.session() as session:
        result = session.run(
            query=cypher,
            parameters={'source_node_id': source_node_id,
                        'target_node_id': target_node_id
                        },
        )
        relationship_data = result.data()[0]

    # Organise the data about the nodes in the relationship
    source_node = Node(node_id=relationship_data['ID(nodeA)'])  # todo: edit

    target_node = Node(node_id=relationship_data['ID(nodeB)'])

    # Return Relationship response
    return Relationship(relationship_id=relationship_data['ID(relationship)'],
                        relationship_type=relationship_data['TYPE(relationship)'],
                        source_node=source_node,
                        target_node=target_node)
