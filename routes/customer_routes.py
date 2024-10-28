from flask import Blueprint, request, jsonify
from db import get_db

customer_bp = Blueprint('customer_bp', __name__)

# Create a new customer
@customer_bp.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    address = data.get('address')
    
    with get_db() as session:
        session.run(
            "CREATE (c:Customer {name: $name, age: $age, address: $address})",
            name=name, age=age, address=address
        )
    
    return jsonify({"message": "Customer created"}), 201

# Get all customers
@customer_bp.route('/customers', methods=['GET'])
def get_customers():
    with get_db() as session:
        result = session.run("MATCH (c:Customer) RETURN c")
        customers = [{"name": record["c"]["name"], "age": record["c"]["age"], "address": record["c"]["address"]} for record in result]
    return jsonify(customers), 200

# Update a customer by ID
@customer_bp.route('/customers/<string:name>', methods=['PUT'])
def update_customer(name):
    data = request.get_json()
    new_age = data.get('age')
    new_address = data.get('address')
    
    with get_db() as session:
        session.run(
            "MATCH (c:Customer {name: $name}) "
            "SET c.age = $age, c.address = $address",
            name=name, age=new_age, address=new_address
        )
    
    return jsonify({"message": "Customer updated"}), 200

# Delete a customer by ID
@customer_bp.route('/customers/<string:name>', methods=['DELETE'])
def delete_customer(name):
    with get_db() as session:
        session.run("MATCH (c:Customer {name: $name}) DELETE c", name=name)
    return jsonify({"message": "Customer deleted"}), 200
