from flask import Blueprint, request, jsonify
from db import get_db

employee_bp = Blueprint('employee_bp', __name__)

# Create a new employee
@employee_bp.route('/employees', methods=['POST'])
def create_employee():
    data = request.get_json()
    name = data.get('name')
    address = data.get('address')
    branch = data.get('branch')
    
    with get_db() as session:
        session.run(
            "CREATE (e:Employee {name: $name, address: $address, branch: $branch})",
            name=name, address=address, branch=branch
        )
    
    return jsonify({"message": "Employee created"}), 201

# Get all employees
@employee_bp.route('/employees', methods=['GET'])
def get_employees():
    with get_db() as session:
        result = session.run("MATCH (e:Employee) RETURN e")
        employees = [{"name": record["e"]["name"], "address": record["e"]["address"], "branch": record["e"]["branch"]} for record in result]
    return jsonify(employees), 200

# Update an employee by ID
@employee_bp.route('/employees/<string:name>', methods=['PUT'])
def update_employee(name):
    data = request.get_json()
    new_address = data.get('address')
    new_branch = data.get('branch')
    
    with get_db() as session:
        session.run(
            "MATCH (e:Employee {name: $name}) "
            "SET e.address = $address, e.branch = $branch",
            name=name, address=new_address, branch=new_branch
        )
    
    return jsonify({"message": "Employee updated"}), 200

# Delete an employee by ID
@employee_bp.route('/employees/<string:name>', methods=['DELETE'])
def delete_employee(name):
    with get_db() as session:
        session.run("MATCH (e:Employee {name: $name}) DELETE e", name=name)
    return jsonify({"message": "Employee deleted"}), 200
