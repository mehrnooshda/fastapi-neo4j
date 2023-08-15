from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class Relationship(BaseModel):
    relationship_id: int
    relationship_type: str
    source_node: None
    target_node: None


# Node response models
class Node(BaseModel):
    label: str
    properties: dict


# class Nodes(BaseModel):
#     nodes: List[Node]


class Query(BaseModel):
    response: list
