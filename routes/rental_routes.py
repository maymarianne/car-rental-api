from flask import Blueprint, request, jsonify
from db import get_db

rental_bp = Blueprint('rental_bp', __name__)

# 1. Order a Car
@rental_bp.route('/order-car', methods=['POST'])
def order_car():
    data = request.get_json()
    customer_id = data['customer_id']
    car_id = data['car_id']
    with get_db() as session:
        # Check if customer has another booking
        existing_booking = session.run(
            """
            MATCH (c:Car {status: 'booked'})<-[:BOOKED_BY]-(cust:Customer)
            WHERE ID(cust) = $customer_id
            RETURN c
            """,
            customer_id=int(customer_id)
        ).single()
        
        if existing_booking:
            return jsonify({"error": "Customer already has a booked car"}), 400
        
        # Book the car if it is available
        result = session.run(
            """
            MATCH (c:Car), (cust:Customer)
            WHERE ID(c) = $car_id AND ID(cust) = $customer_id AND c.status = 'available'
            SET c.status = 'booked'
            CREATE (cust)-[:BOOKED_BY]->(c)
            RETURN c
            """,
            car_id=int(car_id), customer_id=int(customer_id)
        ).single()

        if result:
            return jsonify({"message": "Car successfully booked"}), 200
        else:
            return jsonify({"error": "Car is not available"}), 400

# 2. Cancel Car Order
@rental_bp.route('/cancel-order-car', methods=['POST'])
def cancel_order_car():
    data = request.get_json()
    customer_id = data['customer_id']
    car_id = data['car_id']
    with get_db() as session:
        # Check if the customer has booked the car
        booking = session.run(
            """
            MATCH (cust:Customer)-[r:BOOKED_BY]->(c:Car {status: 'booked'})
            WHERE ID(cust) = $customer_id AND ID(c) = $car_id
            RETURN r
            """,
            customer_id=int(customer_id), car_id=int(car_id)
        ).single()

        if not booking:
            return jsonify({"error": "No booking found for this customer and car"}), 400
        
        # Cancel booking and make car available
        session.run(
            """
            MATCH (cust:Customer)-[r:BOOKED_BY]->(c:Car)
            WHERE ID(cust) = $customer_id AND ID(c) = $car_id
            DELETE r
            SET c.status = 'available'
            """,
            customer_id=int(customer_id), car_id=int(car_id)
        )
        return jsonify({"message": "Booking canceled successfully"}), 200

# 3. Rent a Car
@rental_bp.route('/rent-car', methods=['POST'])
def rent_car():
    data = request.get_json()
    customer_id = data['customer_id']
    car_id = data['car_id']
    with get_db() as session:
        # Check if car is booked by the customer
        booking = session.run(
            """
            MATCH (cust:Customer)-[:BOOKED_BY]->(c:Car {status: 'booked'})
            WHERE ID(cust) = $customer_id AND ID(c) = $car_id
            RETURN c
            """,
            customer_id=int(customer_id), car_id=int(car_id)
        ).single()

        if not booking:
            return jsonify({"error": "Car is not booked by this customer"}), 400

        # Rent the car and update its status to 'rented'
        session.run(
            """
            MATCH (cust:Customer)-[:BOOKED_BY]->(c:Car)
            WHERE ID(cust) = $customer_id AND ID(c) = $car_id
            SET c.status = 'rented'
            """,
            customer_id=int(customer_id), car_id=int(car_id)
        )
        return jsonify({"message": "Car status updated to 'rented'"}), 200

# 4. Return a Car
@rental_bp.route('/return-car', methods=['POST'])
def return_car():
    data = request.get_json()
    customer_id = data['customer_id']
    car_id = data['car_id']
    car_status = data['status']

    # Map "ok" to "available" for consistent car statuses
    if car_status == "ok":
        car_status = "available"
    elif car_status != "damaged":
        return jsonify({"error": "Invalid status provided. Must be 'ok' or 'damaged'."}), 400

    with get_db() as session:
        # Check if car is rented by the customer
        rental = session.run(
            """
            MATCH (cust:Customer)-[:BOOKED_BY]->(c:Car {status: 'rented'})
            WHERE ID(cust) = $customer_id AND ID(c) = $car_id
            RETURN c
            """,
            customer_id=int(customer_id), car_id=int(car_id)
        ).single()

        if not rental:
            return jsonify({"error": "Car is not rented by this customer"}), 400

        # Return the car and set the status accordingly
        session.run(
            """
            MATCH (cust:Customer)-[r:BOOKED_BY]->(c:Car)
            WHERE ID(cust) = $customer_id AND ID(c) = $car_id
            DELETE r
            SET c.status = $car_status
            """,
            customer_id=int(customer_id), car_id=int(car_id), car_status=car_status
        )
        return jsonify({"message": f"Car returned and status updated to '{car_status}'"}), 200
