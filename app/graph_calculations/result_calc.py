from fastapi import APIRouter, HTTPException, status, BackgroundTasks

from app.utils.db import neo4j_driver
from app.utils.schema import Relationship, Node

router = APIRouter()

relationship_types = ['sum', 'subtract', 'divide', 'multiply', 'result']


@router.post('/calculate/{node_id}', response_model=Node)
def calculate_and_store(node_id: int, background_tasks = BackgroundTasks):
    with drive

