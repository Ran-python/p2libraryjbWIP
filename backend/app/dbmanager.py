from flask_sqlalchemy import SQLAlchemy
from app.logger import log_info, log_error, log_debug
from app.LibModels import db, Book, LoanType, Customer, Loan, BookAvailability
from datetime import datetime
from app.auth import auth_bp, init_auth

class DBManager:

   # -------------------------------#
   #        Customer Operations     #
   # -------------------------------#

   @staticmethod
   def create_customer(customer_data):
      try:
            new_customer = Customer(
               name=customer_data['name'],
               city=customer_data.get('city', ''),
               age=customer_data.get('age'),
               phone_number=customer_data.get('phone_number'),
               birth_date=customer_data.get('birth_date'),
               password_hash=customer_data['password_hash'],
               token=customer_data.get('token'),
               active=True
            )
            db.session.add(new_customer)
            db.session.commit()
            log_info(f"Customer {customer_data['name']} added to database")
            return new_customer
      except Exception as e:
            db.session.rollback()
            log_error(f"Error inserting customer into database: {str(e)}")
            return None

   @staticmethod
   def get_customer_by_id(customer_id):
      try:
            return Customer.query.get(customer_id)
      except Exception as e:
            log_error(f"Error fetching customer by ID: {str(e)}")
            return None

   @staticmethod
   def update_customer(customer_id, update_data):
      try:
            customer = Customer.query.get(customer_id)
            if not customer:
               log_error(f"Customer ID {customer_id} not found")
               return None
            for key, value in update_data.items():
               if hasattr(customer, key):
                  setattr(customer, key, value)
            db.session.commit()
            log_info(f"Customer ID {customer_id} updated successfully")
            return customer
      except Exception as e:
            db.session.rollback()
            log_error(f"Error updating customer: {str(e)}")
            return None

   @staticmethod
   def deactivate_customer(customer_id):
      try:
            customer = Customer.query.get(customer_id)
            if not customer:
               log_error(f"Customer ID {customer_id} not found")
               return None
            customer.active = False
            db.session.commit()
            log_info(f"Customer ID {customer_id} deactivated successfully")
            return customer
      except Exception as e:
            db.session.rollback()
            log_error(f"Error deactivating customer: {str(e)}")
            return None

   # -------------------------------#
   #        Book Operations         #
   # -------------------------------#

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

   @staticmethod
   def get_books():
      try:
            log_info("Fetching all books from database")
            return Book.query.all()
      except Exception as e:
            log_error(f"Error fetching books: {str(e)}")
            return []

   @staticmethod
   def update_book(book_id, update_data):
      try:
            book = BookAvailability.query.get(book_id)
            if not book:
               log_error(f"Book ID {book_id} not found")
               return None
            for key, value in update_data.items():
               if hasattr(book, key):
                  setattr(book, key, value)
            db.session.commit()
            log_info(f"Book ID {book_id} updated successfully")
            return book
      except Exception as e:
            db.session.rollback()
            log_error(f"Error updating book: {str(e)}")
            return None

   @staticmethod
   def deactivate_book(book_id):
      try:
            book = BookAvailability.query.get(book_id)
            if not book:
               log_error(f"Book ID {book_id} not found")
               return None
            book.active = False
            db.session.commit()
            log_info(f"Book ID {book_id} deactivated successfully")
            return book
      except Exception as e:
            db.session.rollback()
            log_error(f"Error deactivating book: {str(e)}")
            return None

   # -------------------------------#
   #         Loan Operations        #
   # -------------------------------#

   @staticmethod
   def create_loan(loan_data):
      try:
            new_loan = Loan(
               customer_id=loan_data['customer_id'],
               book_id=loan_data['book_id'],
               loan_date=loan_data['loan_date'],
               due_date=loan_data['due_date'],
               returned=loan_data.get('returned', False)
            )
            db.session.add(new_loan)
            db.session.commit()
            log_info(f"Loan for customer ID {loan_data['customer_id']} created successfully")
            return new_loan
      except Exception as e:
            db.session.rollback()
            log_error(f"Error creating loan: {str(e)}")
            return None

   @staticmethod
   def get_loan_by_id(loan_id):
      try:
            return Loan.query.get(loan_id)
      except Exception as e:
            log_error(f"Error fetching loan by ID: {str(e)}")
            return None

   @staticmethod
   def update_loan(loan_id, update_data):
      try:
            loan = Loan.query.get(loan_id)
            if not loan:
               log_error(f"Loan ID {loan_id} not found")
               return None
            for key, value in update_data.items():
               if hasattr(loan, key):
                  setattr(loan, key, value)
            db.session.commit()
            log_info(f"Loan ID {loan_id} updated successfully")
            return loan
      except Exception as e:
            db.session.rollback()
            log_error(f"Error updating loan: {str(e)}")
            return None

   @staticmethod
   def deactivate_loan(loan_id):
      try:
            loan = Loan.query.get(loan_id)
            if not loan:
               log_error(f"Loan ID {loan_id} not found")
               return None
            loan.active = False
            db.session.commit()
            log_info(f"Loan ID {loan_id} deactivated successfully")
            return loan
      except Exception as e:
            db.session.rollback()
            log_error(f"Error deactivating loan: {str(e)}")
            return None

   @staticmethod
   def get_late_loans():
      try:
            log_info("Fetching late loans")
            return Loan.query.filter(Loan.due_date < datetime.utcnow(), Loan.returned == False).all()
      except Exception as e:
            log_error(f"Error fetching late loans: {str(e)}")
            return []
