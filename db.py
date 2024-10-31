from neo4j import GraphDatabase

# Connection details for Neo4j
uri = "bolt://localhost:7687"
username = "neo4j"  # Default username for Neo4j
password = "assignment4" 

# Initialize the Neo4j driver
driver = GraphDatabase.driver(uri, auth=(username, password))

def get_db():
    """Open a session for Neo4j database access."""
    return driver.session()
