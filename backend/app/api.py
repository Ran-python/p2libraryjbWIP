from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.logger import log_info, log_error, log_warning, log_debug
from app.LibModels import BookAvailability, MyLoan
from app.auth import auth_bp, init_auth
from app.dbmanager import DBManager

# Initialize Blueprint for API routes
api_bp = Blueprint('api', __name__)

# Logging messages
log_info("API Blueprint initialized")

# ------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------

def check_customer_role():
    """Helper function to check if the current user is a customer."""
    current_user = get_jwt_identity()
    if current_user['role'] != 'customer':
        log_error(f"Unauthorized access attempt by {current_user['username']}")
        return jsonify({"error": "Unauthorized access"}), 403
    return current_user

# ------------------------------------------------------------
# Customer Endpoints
# ------------------------------------------------------------

@api_bp.route('/books/available', methods=['GET'])
@jwt_required()
def get_available_books():
    """
    Endpoint to get the list of available books.
    Accessible only to customers.
    """
    current_user = check_customer_role()
    if isinstance(current_user, tuple):  # if an error response, return it
        return current_user

    books = DBManager.get_books()
    book_list = [
        {
            "book_id": book.book_id,
            "book_name": book.book_name,
            "author": book.author,
            "year_published": book.year_published,
            "loan_type": book.loan_type,
            "availability_status": book.availability_status
        } for book in books
    ]
    log_info(f"Customer {current_user['username']} accessed available books")
    return jsonify(book_list), 200

@api_bp.route('/my-loans', methods=['GET'])
@jwt_required()
def get_my_loans():
    """
    Endpoint for customers to view their own loans.
    """
    current_user = check_customer_role()
    if isinstance(current_user, tuple):
        return current_user

    my_loans = MyLoan.query.filter_by(cust_id=current_user['id']).all()
    loan_list = [
        {
            "loan_id": loan.loan_id,
            "book_id": loan.book_id,
            "book_name": loan.book_name,
            "author": loan.author,
            "loan_date": loan.loan_date.strftime("%Y-%m-%d"),
            "return_date": loan.return_date.strftime("%Y-%m-%d") if loan.return_date else None,
            "is_loaned": loan.is_loaned
        } for loan in my_loans
    ]
    log_info(f"Customer {current_user['username']} accessed their loans")
    return jsonify(loan_list), 200

# ------------------------------------------------------------
# Book Management (CRUD)
# ------------------------------------------------------------

@api_bp.route('/books', methods=['POST', 'GET'])
@jwt_required()
def handle_books():
    try:
        if request.method == 'POST':
            # Extract book data from request
            book_data = request.get_json()
            log_info(f"Received book creation request: {book_data}")

            # Forward the data to DBManager for processing
            new_book = DBManager.create_book(book_data)
            if new_book:
                return jsonify(new_book.to_dict()), 201
            else:
                return jsonify({"error": "Failed to add book"}), 400

        elif request.method == 'GET':
            books = DBManager.get_books()
            book_list = [book.to_dict() for book in books]
            return jsonify(book_list), 200

    except Exception as e:
        log_error(f"Error processing book request: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# ------------------------------------------------------------
# Admin Endpoints
# ------------------------------------------------------------

@api_bp.route('/admin', methods=['GET'])
@jwt_required()
def admin_dashboard():
    """
    Endpoint for the admin dashboard.
    Accessible only to librarians.
    """
    current_user = get_jwt_identity()
    if current_user['role'] != 'librarian':
        log_error(f"Unauthorized access attempt by {current_user['username']} to admin dashboard")
        return jsonify({"error": "Access forbidden"}), 403
    return jsonify({"message": "Welcome to the admin dashboard!"})

# ------------------------------------------------------------
# User Endpoints
# ------------------------------------------------------------

@api_bp.route('/user-data', methods=['GET'])
@jwt_required()
def user_dashboard():
    """
    Endpoint for users to view their dashboard.
    """
    current_user = get_jwt_identity()
    return jsonify({"message": f"Welcome {current_user['username']}!"})
