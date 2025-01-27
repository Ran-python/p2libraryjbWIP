from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from werkzeug.security import generate_password_hash, check_password_hash
from app.LibModels import db, BookAvailability, Loan, Customer, Book
from app.logger import log_info, log_error, log_warning
from config.config import Config
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

# Initialize JWT
jwt = JWTManager()

# Static mapping of librarian username
LIBRARIAN_USERNAME = "Ran"  # Librarian root user

# Function to initialize JWT in the Flask app
def init_auth(app):
    app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
    jwt.init_app(app)

def is_admin_or_root():
    current_user = get_jwt_identity()
    if current_user['role'] not in ['librarian', 'root']:
        return False
    return True

# Customer CRUD operations
@auth_bp.route('/customers', methods=['POST'])
@jwt_required()
def signup():
    if not is_admin_or_root():
        return jsonify({"error": "Unauthorized access"}), 403
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({"error": "Missing required fields"}), 400
        
        if Customer.query.filter_by(name=data['username']).first():
            return jsonify({"error": "User already exists"}), 409
        
        hashed_password = generate_password_hash(data['password'])
        access_token = create_access_token(identity={'username': data['username'], 'role': 'customer'})
        
        new_customer = Customer(
            name=data['username'],
            city=data.get('city', ''),
            age=data.get('age'),
            phone_number=data.get('phone_number'),
            birth_date=data.get('birth_date'),
            password_hash=hashed_password,
            token=access_token,
            active=True
        )
        db.session.add(new_customer)
        db.session.commit()

        return jsonify({"message": "User registered successfully", "access_token": access_token}), 201

    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@auth_bp.route('/customers/<int:id>', methods=['GET'])
@jwt_required()
def get_customer(id):
    if not is_admin_or_root():
        return jsonify({"error": "Unauthorized access"}), 403
    customer = Customer.query.get_or_404(id)
    return jsonify(customer.to_dict())

@auth_bp.route('/customers/<int:id>', methods=['PUT'])
@jwt_required()
def update_customer(id):
    if not is_admin_or_root():
        return jsonify({"error": "Unauthorized access"}), 403
    data = request.get_json()
    customer = Customer.query.get_or_404(id)
    for key, value in data.items():
        if hasattr(customer, key):
            setattr(customer, key, value)
    db.session.commit()
    return jsonify(customer.to_dict())

@auth_bp.route('/customers/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_customer(id):
    if not is_admin_or_root():
        return jsonify({"error": "Unauthorized access"}), 403
    customer = Customer.query.get_or_404(id)
    customer.active = False
    db.session.commit()
    return jsonify({"message": "Customer deactivated"})

# Book CRUD operations
@auth_bp.route('/books', methods=['POST'])
@jwt_required()
def add_book():
    if not is_admin_or_root():
        return jsonify({"error": "Unauthorized access"}), 403
    data = request.get_json()
    new_book = Book(**data)
    db.session.add(new_book)
    db.session.commit()
    return jsonify(new_book.to_dict()), 201

@auth_bp.route('/books/<int:id>', methods=['GET'])
@jwt_required()
def get_book(id):
    if not is_admin_or_root():
        return jsonify({"error": "Unauthorized access"}), 403
    book = Book.query.get_or_404(id)
    return jsonify(book.to_dict())

@auth_bp.route('/books/<int:id>', methods=['PUT'])
@jwt_required()
def update_book(id):
    if not is_admin_or_root():
        return jsonify({"error": "Unauthorized access"}), 403
    data = request.get_json()
    book = Book.query.get_or_404(id)
    for key, value in data.items():
        if hasattr(book, key):
            setattr(book, key, value)
    db.session.commit()
    return jsonify(book.to_dict())

@auth_bp.route('/books/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_book(id):
    if not is_admin_or_root():
        return jsonify({"error": "Unauthorized access"}), 403
    book = Book.query.get_or_404(id)
    book.active = False
    db.session.commit()
    return jsonify({"message": "Book deactivated"})

# Loan CRUD operations
@auth_bp.route('/loans', methods=['POST'])
@jwt_required()
def add_loan():
    if not is_admin_or_root():
        return jsonify({"error": "Unauthorized access"}), 403
    data = request.get_json()
    new_loan = Loan(**data)
    db.session.add(new_loan)
    db.session.commit()
    return jsonify(new_loan.to_dict()), 201

@auth_bp.route('/loans/<int:id>', methods=['GET'])
@jwt_required()
def get_loan(id):
    if not is_admin_or_root():
        return jsonify({"error": "Unauthorized access"}), 403
    loan = Loan.query.get_or_404(id)
    return jsonify(loan.to_dict())

@auth_bp.route('/loans/<int:id>', methods=['PUT'])
@jwt_required()
def update_loan(id):
    if not is_admin_or_root():
        return jsonify({"error": "Unauthorized access"}), 403
    data = request.get_json()
    loan = Loan.query.get_or_404(id)
    for key, value in data.items():
        if hasattr(loan, key):
            setattr(loan, key, value)
    db.session.commit()
    return jsonify(loan.to_dict())

@auth_bp.route('/loans/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_loan(id):
    if not is_admin_or_root():
        return jsonify({"error": "Unauthorized access"}), 403
    loan = Loan.query.get_or_404(id)
    loan.active = False
    db.session.commit()
    return jsonify({"message": "Loan deactivated"})

@auth_bp.route('/loans/late', methods=['GET'])
@jwt_required()
def check_late_loans():
    if not is_admin_or_root():
        return jsonify({"error": "Unauthorized access"}), 403
    late_loans = Loan.query.filter(Loan.due_date < datetime.utcnow(), Loan.returned == False).all()
    return jsonify([loan.to_dict() for loan in late_loans])
