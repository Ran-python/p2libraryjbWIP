from logging import root
from os import name
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from werkzeug.security import generate_password_hash, check_password_hash
from app.LibModels import db, Customer
from app.logger import log_info, log_error, log_warning
from config.config import Config
from datetime import datetime


auth_bp = Blueprint('auth', __name__)


# Initialize JWT
jwt = JWTManager()

# Static mapping of librarian username
root = LIBRARIAN_USERNAME = "Ran"  # Librarian root user

@auth_bp.route('/customers', methods=['POST'])
def signup():
    try:
        data = request.get_json()

        if not data or 'username' not in data or 'password' not in data or 'city' not in data:
            log_error("Invalid signup attempt - missing fields")
            return jsonify({"error": "Missing required fields"}), 400

        # Check for duplicate user
        existing_user = Customer.query.filter_by(name=data['username']).first()
        if existing_user:
            log_error(f"Signup failed - User {data['username']} already exists")
            return jsonify({"error": "User already exists"}), 409

        # Generate JWT token with unique timestamp
        access_token = create_access_token(identity={
            'username': data['username'],
            'role': 'customer',
            'timestamp': str(datetime.utcnow())  # Ensuring uniqueness
        })

        # Check for duplicate token
        existing_token = Customer.query.filter_by(token=access_token).first()
        if existing_token:
            log_warning(f"Token already exists for user {existing_token.name}, generating new token.")
            return jsonify({"error": "Duplicate token detected"}), 400

        # Hash the password before storing it
        hashed_password = generate_password_hash(data['password'])

        # Create new customer
        new_customer = Customer(
            name=data['username'],
            city=data.get('city', ''),
            age=data.get('age'),
            phone_number=data.get('phone_number'),
            birth_date=data.get('birth_date'),
            password_hash=hashed_password,
            token=access_token,  # Store token in the database
            active=True  # Set active status to True
        )

        db.session.add(new_customer)
        db.session.commit()

        log_info(f"New user {data['username']} registered successfully")

        # Ensure the token is included in the response
        return jsonify({
            "message": "User registered successfully",
            "access_token": access_token
        }), 201

    except Exception as e:
        log_error(f"Signup error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        # Find active user by username
        user = Customer.query.filter_by(name=data['username'], active=True).first()

        if not user or not check_password_hash(user.password_hash, data['password']):
            log_error("Invalid username or password")
            return jsonify({"error": "Invalid username or password"}), 401

        # Invalidate old token (optional security measure)
        if user.token:
            log_info(f"User {user.name} had an active session, revoking old token.")
            user.token = None  # Clear old token before issuing a new one
            db.session.commit()

        # Assign role based on username
        role = "librarian" if user.name == LIBRARIAN_USERNAME else "customer"

        # Generate JWT token with expiration time
        access_token = create_access_token(identity={'username': user.name, 'role': role})

        # Store token in the database
        user.token = access_token
        db.session.commit()

        log_info(f"User {user.name} logged in successfully as {role}")
        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "role": role
        }), 200

    except Exception as e:
        log_error(f"Login error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


# Function to initialize JWT in the Flask app
def init_auth(app):
    app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
    jwt.init_app(app)

# read all customers
@auth_bp.route('/customers', methods=['GET'])
def customers():
    try:
        customers = Customer.query.all()
        db.session.commit()
        print(customers)
        return jsonify([customer.to_dict() for customer in customers])
        # return jsonify([customers.to_dict() for customer in customers])
    finally:
        print('done')

# find by id
@auth_bp.route('/customers/<int:id>', methods=['GET'])
def customersById(id):
    try:
        # customer_id = request.args.get('id', type=int)
        print("Customer id : "+str(id))
        c = Customer.query.filter_by(id=id).first()
        return jsonify(c.to_dict())
        # return jsonify([item.to_dict() for item in c])
    finally:
        print('done')

#delete customer (make not active) 
@auth_bp.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    try:
        # customer_id = request.args.get('id', type=int)
        cust = Customer.query.get(id)
        setattr(cust, "active",False)
        db.session.commit()
        print(cust)
        return jsonify(cust.to_dict())
    finally:
        print('done')
        
#update customer
@auth_bp.route('/customers/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        data = request.get_json()
        cust = Customer.query.get(id)
        for field, value in data.items():
            if hasattr(cust, field):
                setattr(cust, field, value)
        
        db.session.commit()
        return 'ok'
    finally:
        print("Done")
