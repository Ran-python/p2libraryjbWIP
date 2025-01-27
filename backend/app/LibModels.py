from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# User Model (For authentication purposes)
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


# LoanType Model with predefined loan periods
class LoanType(db.Model):
    __tablename__ = 'loantypes'
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(100), nullable=False, unique=True)
    max_days = db.Column(db.Integer, nullable=False)

    books = db.relationship('Book', back_populates='loan_type', lazy=True)

    @staticmethod
    def seed_loan_types():
        """Seed the database with predefined loan types."""
        loan_types = [
            LoanType(type_name="Short Term", max_days=2),
            LoanType(type_name="Medium Term", max_days=5),
            LoanType(type_name="Long Term", max_days=10)
        ]
        db.session.bulk_save_objects(loan_types)
        db.session.commit()

    def __repr__(self):
        return f"<LoanType {self.type_name} ({self.max_days} days)>"


# Book Model with a relationship to LoanType and Loan
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    year_published = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(500))
    active = db.Column(db.Boolean, default=True)

    # Relationship with LoanType
    loan_type_id = db.Column(db.Integer, db.ForeignKey('loantypes.id'), nullable=False)
    loan_type = db.relationship('LoanType', back_populates='books')

    # Relationship with Loans (a book can have multiple loans)
    loans = db.relationship('Loan', back_populates='book')

    def deactivate(self):
        """Deactivate the book."""
        self.active = False

    def __repr__(self):
        return f"<Book {self.name} by {self.author}>"


# Customer Model
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    city = db.Column(db.String(100))
    age = db.Column(db.Integer)
    phone_number = db.Column(db.String(20))
    birth_date = db.Column(db.Date)
    password_hash = db.Column(db.String(200), nullable=False)
    token = db.Column(db.String(500))  # Optional token storage
    active = db.Column(db.Boolean, default=True)

    # Relationship with Loans (a customer can have multiple loans)
    loans = db.relationship('Loan', back_populates='customer')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def deactivate(self):
        """Deactivate the customer account."""
        self.active = False

    def activate(self):
        """Activate the customer account."""
        self.active = True

    def __repr__(self):
        return f"<Customer {self.name}, Active: {self.active}>"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'active': self.active
        }

# Loan Model
class Loan(db.Model):
    __tablename__ = 'loans'
    id = db.Column(db.Integer, primary_key=True)
    cust_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    loan_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    return_date = db.Column(db.DateTime)
    is_loaned = db.Column(db.Boolean, default=True)
    active = db.Column(db.Boolean, default=True)

    # Relationships
    customer = db.relationship('Customer', back_populates='loans')
    book = db.relationship('Book', back_populates='loans')

    def mark_returned(self):
        """Mark the loan as returned."""
        self.is_loaned = False
        self.active = False
        self.return_date = datetime.utcnow()

    def __repr__(self):
        return f"<Loan Customer ID {self.cust_id} Book ID {self.book_id}>"


# MyLoan Model (for tracking customer-specific book loans)
class MyLoan(db.Model):
    __tablename__ = 'my_loans'
    loan_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    book_name = db.Column(db.String(255))
    author = db.Column(db.String(255))
    loan_date = db.Column(db.DateTime)
    return_date = db.Column(db.DateTime)
    is_loaned = db.Column(db.Boolean, default=True)
    active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<MyLoan Loan ID {self.loan_id} Book Name {self.book_name}>"


# BookAvailability Model (for tracking book availability)
class BookAvailability(db.Model):
    __tablename__ = 'bookavailability'
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), primary_key=True)
    book_name = db.Column(db.String(255))
    author = db.Column(db.String(255))
    year_published = db.Column(db.Integer)
    image_url = db.Column(db.String(500))
    loan_type = db.Column(db.String(100))
    return_date = db.Column(db.DateTime)
    availability_status = db.Column(db.String(50))

    def __repr__(self):
        return f"<BookAvailability {self.book_name} Status {self.availability_status}>"
