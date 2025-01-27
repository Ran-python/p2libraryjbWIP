from app.logger import log_info, log_error, log_warning, log_debug
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager
from app.LibModels import db, Book, LoanType, Customer, Loan, MyLoan, BookAvailability, User
from flask import Flask, jsonify
from app.dbmanager import DBManager

data = DBManager

# Initialize Flask app
app = Flask(__name__)

# Configure JWT
app.config['JWT_SECRET_KEY'] = 'supersecretkey'  # Ensure to replace this with a secure value
jwt = JWTManager(app)

log_info("Flask application is starting")
log_debug("Debugging application configuration")
log_warning("This is a warning")
log_error("An error occurred while processing")

class BusinessLayer:
    
    @staticmethod
    @jwt_required()
    def get_books():
        current_user = get_jwt_identity()
        log_info(f"Fetching books for {current_user['username']} ({current_user['role']})")
        try:
            books = Book.query.all()
            book_list = [{"id": book.id, "name": book.name, "author": book.author} for book in books]
            return jsonify({"books": book_list}), 200
        except Exception as e:
            log_error(f"Error retrieving books: {str(e)}")
            return jsonify({"error": "Failed to retrieve books"}), 500

class Businesslayer:
    """Handles CRUD operations for books."""
    
class BusinessLayer:
    
    @staticmethod
    def add_book(book_data):
        try:
            # Ensure required fields are present
            required_fields = ['book_name', 'author', 'year_published', 'loan_type']
            for field in required_fields:
                if field not in book_data or not book_data[field]:
                    log_error(f"Missing field: {field}")
                    return {"error": f"Field '{field}' is required"}, 400

            # Authorization check (only root users allowed)
            current_user = get_jwt_identity()
            if current_user['role'] != 'root':
                log_error("Unauthorized access attempt")
                return {"error": "Unauthorized access"}, 403

            new_book = BookAvailability(
                book_name=book_data['book_name'],
                author=book_data['author'],
                year_published=book_data['year_published'],
                loan_type=book_data['loan_type']
            )

            db.session.add(new_book)
            db.session.commit()

            log_info(f"Book {book_data['book_name']} added successfully")
            return {"message": "Book added successfully"}, 201

        except Exception as e:
            db.session.rollback()
            log_error(f"Error adding book: {str(e)}")
            return {"error": "Failed to add book"}, 500
        
    #@staticmethod
    #def get_books():
        #print("this line gets all books from dbmanager.py")
        #print("this line validates data(do i have data? is the request correct?)")
        #print("this line returns data back to api.py")

@app.route('/business/books', methods=['GET'])
@jwt_required()
def handle_get_books():
    """API route to get books via business layer."""
    return BusinessLayer.get_books()

if __name__ == "__main__":
    app.run(debug=True, port=5001)