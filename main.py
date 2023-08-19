from fastapi import  FastAPI
from app.graph import crud
from app.graph_calculations import result_calc

app = FastAPI(title='Graph-Based Calculation Microservice',
              description='a Python microservice that performs calculations using data stored in a Neo4j graph database',
              docs_url='/docs')

app.include_router(
    crud.router,
    prefix='/crud',
    # tags=['Graph Objects'],
)

app.include_router(
    result_calc.router,
    prefix='/result'
)
