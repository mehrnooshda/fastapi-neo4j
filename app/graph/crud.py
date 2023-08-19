from fastapi import APIRouter, HTTPException, status

from app.utils.db import neo4j_driver
from app.utils.schema import Relationship, Node

router = APIRouter()

relationship_types = ['sum', 'subtract', 'divide', 'multiply', 'result']


@router.get('/node/{node_id}', response_model=Node)  # todo: create when method is post (error handling)
def retrieve_node(node_id: int):
    cypher = """
    MATCH (node) 
    WHERE ID(node) = $node_id
    return id(node) as id, labels(node) as label, properties(node) as properties
    """
    with neo4j_driver.session() as session:
        result = session.run(query=cypher,
                             parameters={'node_id': node_id})

        result_data = result.data()
        if not result_data or result_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Node not found.")
        node_data = result_data[0]

    return Node(node_id=node_data['id'],
                label=node_data['label'][0],
                properties=node_data['properties'])


@router.post('/node', response_model=Node)
def create_node(label: str, node_attributes: dict):
    unpacked_attributes = ', '.join(f'new_node.{key} = \'{value}\'' for (key, value) in node_attributes.items())
    cypher = f"""
            CREATE (new_node:{label})
            SET {unpacked_attributes}
            RETURN new_node,
             LABELS(new_node) as label, ID(new_node) as id,  properties(new_node) as properties
            """

    with neo4j_driver.session() as session:
        result1 = session.run(
            query=cypher,
            parameters={
                'attributes': node_attributes
            },
        )
        node_data = result1.data()[0]
        # print('node_data', node_data)
        # print("Node Data:", node_data['new_node'])
        # print("Labels:", node_data['label'])
        # print("Node ID:", node_data['id'])

    return Node(node_id=node_data['id'],
                label=node_data['label'][0],
                properties=node_data['new_node'])


@router.post('/create_relationship', response_model=Relationship)
def create_relationship(source_node_id, target_node_id, relationship_type):
    if relationship_type not in relationship_types:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Permission denied, relationship type is not acceptable",
            headers={"WWW-Authenticate": "Bearer"}
        )
    print('..........', source_node_id, target_node_id, relationship_type)
    # label = 'A'
    # unpacked_attributes = {'un': 'packed'}

    cypher = f"""
        MATCH (sourceNode) WHERE ID(sourceNode) = {source_node_id}
        MATCH (targetNode) WHERE ID(targetNode) = {target_node_id}
        CREATE (sourceNode)-[relationship:%s]->(targetNode)

        RETURN sourceNode, targetNode, ID(sourceNode) as source_id, ID(targetNode) as target_id,
        labels(sourceNode) as source_label, labels(targetNode) as target_label, properties(sourceNode) as source_properties,
        properties(targetNode) as target_properties, ID(relationship) as relationship_id, TYPE(relationship) as rel_type
        """ % relationship_type
    with neo4j_driver.session() as session:
        result = session.run(
            query=cypher,
            parameters={'source_node_id': source_node_id,
                        'target_node_id': target_node_id,
                        'relationship_type': relationship_type
                        }
        )

        relationship_data = result.data()[0]

    # Organise the data about the nodes in the relationship
    source_node = Node(node_id=relationship_data['source_id'],
                       label=relationship_data['source_label'][0],
                       properties=relationship_data['source_properties']
                       )  # todo: edit
    target_node = Node(node_id=relationship_data['target_id'],
                       label=relationship_data['target_label'][0],
                       properties=relationship_data['target_properties']
                       )

    # Return Relationship response
    return Relationship(relationship_id=relationship_data['relationship_id'],
                        relationship_type=relationship_data['rel_type'],
                        source_node=source_node,
                        target_node=target_node)
