import os
from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:***********@localhost/p2libraryjb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Secret Key - Using environment variable with a fallback for security and token expiry
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'supersecretkey')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Set token expiration


# Define the path to the instance folder within the backend directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'instance'))
print(f"This is our directory {INSTANCE_DIR}")

# Ensure instance directory exists
try:
    os.makedirs(INSTANCE_DIR, exist_ok=True)
except Exception as e:
    print(f"Error creating instance directory: {e}")







