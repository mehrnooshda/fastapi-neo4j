# Project README

## Graph-Based Calculation Microservice

This project is a Python microservice that performs calculations using data stored in a Neo4j graph database. The microservice is built using FastAPI (and is supposed to support background tasks for processing).

### Requirements

- Python
- FastAPI
- Neo4j
- neo4j Python driver or an appropriate library

### Project Structure

The project structure is as follows:
```
fastapi-neo4j/
├── app/
│   ├── graph/
│   │   ├── __init__.py
│   │   └── crud.py
│   ├── graph-calculations/
│   │   ├── __init__.py
│   │   └── calculations.py
│   ├── __init__.py
│   └── utils/
│       ├── __init__.py
│       ├── db.py
│       └── schema.py
├── .env
├── requirements.txt
└── main.py
```

The `app` directory contains the main application code. The `graph` package handles the CRUD operations for interacting with the Neo4j graph database. The `graph-calculations` package contains the calculations related endpoints. The `utils` package contains the schema definitions and the database initialization code.

### Endpoints

The microservice provides the following endpoints:

#### Endpoint 1: /node/{node_id} (GET)

Retrieve a specific node from the Neo4j graph database based on the provided `node_id`.

#### Endpoint 2: /node (POST)

Create a new node in the Neo4j graph database. The endpoint should accept a `label` parameter for the node label and `node_attributes` parameter for the node properties.

#### Endpoint 3: /create_relationship (POST)

Create a relationship between two existing nodes in the Neo4j graph database. The endpoint should accept `source_node_id`, `target_node_id`, and `relationship_type` parameters.

#### Endpoint 4: /calculate/{node_id} (POST)

Perform a calculation using data from the specified node and its related nodes in the graph. The calculation should involve traversing the graph and aggregating data from connected nodes. Store the calculated result in the database as a new node connected to the original node with a specific relationship type.
Unfortunately, this endpoint has not been completed yet as I have not received any responses from the task assigner.

#### Endpoint 5: /result/{node_id} (GET)

Retrieve the calculated result node associated with the data node with the provided `node_id`.
Unfortunately, this endpoint has not been completed yet as I have not received any responses from the task assigner.


### How to Run the Microservice Locally

1. Clone the repository: `git clone `
2. Install the dependencies: `pip install -r requirements.txt`
3. Set up the Neo4j database and update the connection details in the `.env` file.
4. Run the microservice: `uvicorn main:app --reload`
5. Get the endpoints by adding /docs at the end of base_url


