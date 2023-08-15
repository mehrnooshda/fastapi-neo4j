from fastapi import  FastAPI
from app.graph import crud
app = FastAPI(title='Graph-Based Calculation Microservice',
              description='a Python microservice that performs calculations using data stored in a Neo4j graph database',
              docs_url='/docs')

app.include_router(
    crud.router,
    prefix='/graph',
    # tags=['Graph Objects'],

)