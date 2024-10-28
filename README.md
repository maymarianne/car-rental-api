# Car Rental API

This project implements a car rental system using Flask and Neo4j. The system allows customers to rent cars for an unlimited time. The functionalities include creating, reading, updating, and deleting cars, customers, and employees, as well as managing car rentals.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
- [Testing with Postman](#testing-with-postman)
- [License](#license)

## Project Overview

This project was created as part of the INFO212 System Development course to practice Web API development, database interaction with Neo4j, and collaborative version control using Git and GitHub. The goal is to create a system for managing a car rental service where customers can rent, book, and return cars.

## Features

- CRUD operations for:
  - Cars (e.g., add, update, delete car details)
  - Customers (e.g., add, update, delete customer details)
  - Employees (e.g., add, update, delete employee details)
- Renting, booking, and returning cars with status updates.

## Setup Instructions

### Prerequisites

- **Python 3.8+**
- **Neo4j** installed locally or accessible via a remote server
- **Postman** (for testing the API)

### Installation Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Neo4j Database:**
   - Ensure Neo4j is running.
   - Update `db.py` with your Neo4j credentials if they differ from the default.

5. **Run the Application:**
   ```bash
   flask run
   ```
   The API should now be running at `http://127.0.0.1:5000`.

## API Endpoints

Here’s a summary of available endpoints:

### Cars
- **Create a Car**: `POST /cars` – Add a new car to the system.
- **Read Cars**: `GET /cars` – Retrieve a list of cars.
- **Update a Car**: `PUT /cars/<car_id>` – Update car details.
- **Delete a Car**: `DELETE /cars/<car_id>` – Remove a car from the system.

### Customers
- **Create a Customer**: `POST /customers`
- **Read Customers**: `GET /customers`
- **Update a Customer**: `PUT /customers/<customer_id>`
- **Delete a Customer**: `DELETE /customers/<customer_id>`

### Employees
- **Create an Employee**: `POST /employees`
- **Read Employees**: `GET /employees`
- **Update an Employee**: `PUT /employees/<employee_id>`
- **Delete an Employee**: `DELETE /employees/<employee_id>`

### Rental Operations
- **Order a Car**: `POST /order-car` – Book a car for a customer if available.
- **Cancel Car Order**: `POST /cancel-order-car` – Cancel a customer's car booking.
- **Rent a Car**: `POST /rent-car` – Rent a booked car to the customer.
- **Return a Car**: `POST /return-car` – Return a rented car with status update (available or damaged).

## Testing with Postman

To test the API:

1. Open Postman and set up requests to the endpoints above.
2. Use JSON format in the request body for POST and PUT requests.
3. Examples:
   - **Creating a Car**:
     ```json
     {
       "make": "Jaguar",
       "model": "X-Type",
       "year": 2003,
       "location": "Downtown",
       "status": "available"
     }
     ```
   - **Ordering a Car**:
     ```json
     {
       "customer_id": 6,
       "car_id": 1
     }
     ```
