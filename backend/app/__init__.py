from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.config import Config
from app.logger import log_info, log_error, log_warning, log_debug

# Logging
log_info("Flask application is starting")
log_debug("Debugging application configuration")
log_warning("This is a warning")
log_error("An error occurred while processing")

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)
    print("Using database:", app.config['SQLALCHEMY_DATABASE_URI'])

    # Initialize the database
    db.init_app(app)

    with app.app_context():
        # Correct import of models from app.LibModels
        from app.LibModels import Book, LoanType, Customer, Loan, MyLoan, BookAvailability
        db.create_all()
        print("Database tables created successfully!")

    return app
