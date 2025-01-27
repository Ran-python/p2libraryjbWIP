from flask import Flask, request
from app.LibModels import db, BookAvailability, LoanType
from app.api import api_bp
from config.config import Config
from app.logger import log_info, log_error, log_warning, log_debug
from flask_jwt_extended import JWTManager
from app.auth import auth_bp, init_auth  # Import auth blueprint and initialization
from app.businesslayer import app as business_app
from flask_cors import CORS  # Optional for cross-origin requests



# Define Flask app 
app = Flask(__name__)
app.config.from_object(Config)
app.config['JWT_SECRET_KEY'] = 'supersecretkey'  # Set a strong secret key for JWT

# Initialize JWT
jwt = JWTManager(app)

# Initialize authentication system
init_auth(app)

# Enable CORS (optional)
CORS(app)

app.logger.info("Flask application is starting")
app.logger.warning("This is a warning")
app.logger.error("An error occurred while processing")

# Define class shortcuts
BookList = BookAvailability

# Load configuration settings
print("Using database:", app.config['SQLALCHEMY_DATABASE_URI'])
print("Using instance path:", app.instance_path)

# Initialize SQLAlchemy with Flask app
db.init_app(app)

# Register blueprints for authentication and API
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/')
def home():
    log_info("Home route accessed", request.remote_addr)
    return "Welcome to the home page!"

# Ensure database tables are created
with app.app_context():
    db.create_all()
    LoanType.seed_loan_types()
    print("Database tables created and loan types seeded successfully!")

if __name__ == "__main__":
    log_info("Starting Flask application")
    print("JWT secret key is set.")

    # Start the Flask app
    app.run(debug=True, port=5000, use_reloader=False)

    # Start the business logic service separately (optional)
    # Consider threading if you want both apps running together.
