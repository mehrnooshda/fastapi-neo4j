from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime






# Node response models
class Node(BaseModel):
    label: str
    properties: dict


class Relationship(BaseModel):
    relationship_id: int
    relationship_type: str
    source_node: Node
    target_node: Node

# class Nodes(BaseModel):
#     nodes: List[Node]


class Query(BaseModel):
    response: list
