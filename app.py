from flask import Flask
from routes.car_routes import car_bp
from routes.customer_routes import customer_bp
from routes.employee_routes import employee_bp
from routes.rental_routes import rental_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(car_bp)
app.register_blueprint(customer_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(rental_bp)

@app.route('/')
def home():
    return {"message": "Car Rental API is running"}

if __name__ == '__main__':
    app.run(debug=True)
