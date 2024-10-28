from flask import Flask, jsonify, request
from neo4j import GraphDatabase

# Initialize Flask app
app = Flask(__name__)

# Set up Neo4j connection
uri = "bolt://localhost:7687"
username = "neo4j"  # Change this if your username is different
password = "assignment4"

# Initialize the Neo4j driver
driver = GraphDatabase.driver(uri, auth=(username, password))

def get_db():
    """Function to open a Neo4j session."""
    return driver.session()

# Route to test if the API is running
@app.route('/')
def home():
    return jsonify({"message": "Car Rental API is running"})

# Route to test Neo4j connection
@app.route('/test-db')
def test_db():
    """Test route to confirm connection to Neo4j."""
    with get_db() as session:
        result = session.run("MATCH (n) RETURN n LIMIT 5")
        nodes = [record["n"] for record in result]
    return jsonify([str(node) for node in nodes])

if __name__ == '__main__':
    app.run(debug=True)
