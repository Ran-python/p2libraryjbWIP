from re import S
from flask_sqlalchemy import SQLAlchemy 
from flask import Flask
from app.logger import log_info, log_error, log_warning, log_debug
from app.LibModels import db, Book, LoanType, Customer, Loan, MyLoan, BookAvailability, User

log_info("Flask application is starting")
log_debug("Debugging application configuration")
log_warning("This is a warning")
log_error("An error occurred while processing")

# Initialize Flask app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:yourpassword@localhost/p2libraryjb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the Flask app context
db.init_app(app)

## Ensure database tables are created
with app.app_context():db.create_all()
print("Database tables created successfully!")
print("Database tables created successfully!")

# -------------------------------#
#        CRUD Operations         #
# -------------------------------#

class DBManager:

   @staticmethod
   def create_book(book_data):
         try:
            new_book = BookAvailability(
               book_name=book_data['book_name'],
               author=book_data['author'],
               year_published=book_data['year_published'],
               loan_type=book_data['loan_type']
            )
            db.session.add(new_book)
            db.session.commit()
            log_info(f"Book {book_data['book_name']} added to database")
            return new_book
         except Exception as e:
            db.session.rollback()
            log_error(f"Error inserting book into database: {str(e)}")
            return None


# Methods like get_books/return_books
class DBManager:
   @staticmethod
   def get_books():
      log_info("Connecting to database")
      # Example query to fetch all books from the database
      books = Book.query.all()
      return books

