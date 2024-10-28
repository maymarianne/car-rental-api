from flask import Blueprint, request, jsonify
from db import get_db

car_bp = Blueprint('cars', __name__)

# Create a new car
@car_bp.route('/cars', methods=['POST'])
def create_car():
    data = request.get_json()
    with get_db() as session:
        session.run("CREATE (c:Car {make: $make, model: $model, year: $year, location: $location, status: $status}) RETURN c",
                    make=data['make'], model=data['model'], year=data['year'], location=data['location'], status=data['status'])
    return jsonify({"message": "Car created"}), 201

# Get all cars
@car_bp.route('/cars', methods=['GET'])
def get_cars():
    with get_db() as session:
        result = session.run("MATCH (c:Car) RETURN c")
        cars = [{"make": record["c"]["make"], "model": record["c"]["model"], "year": record["c"]["year"], "location": record["c"]["location"], "status": record["c"]["status"]} for record in result]
    return jsonify(cars), 200

# Update a car by ID
@car_bp.route('/cars/<car_id>', methods=['PUT'])
def update_car(car_id):
    data = request.get_json()
    with get_db() as session:
        session.run("MATCH (c:Car) WHERE ID(c) = $car_id SET c.make = $make, c.model = $model, c.year = $year, c.location = $location, c.status = $status RETURN c",
                    car_id=int(car_id), make=data['make'], model=data['model'], year=data['year'], location=data['location'], status=data['status'])
    return jsonify({"message": "Car updated"}), 200

# Delete a car by ID
@car_bp.route('/cars/<car_id>', methods=['DELETE'])
def delete_car(car_id):
    with get_db() as session:
        session.run("MATCH (c:Car) WHERE ID(c) = $car_id DELETE c", car_id=int(car_id))
    return jsonify({"message": "Car deleted"}), 200
