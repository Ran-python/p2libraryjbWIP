## passwords
### general user or root: yourpassword
### local host or p2user which has all GRANTS: your_new_password
### user password for user interface: user_password
### USER 'cust_user'@'%' IDENTIFIED BY 'secure_password';

## technologies
# flask
# must use flask_cors to connect to front and back
# jws if you want
# oop - ABC
# from datetime import datetime, timedelta
# sqlalchemy to mySQL DB
# logger with time , date (use line n.12 in readme.md as import),ip adress , and MAYBE where the user came from AND location 
# toastify or toast (same)
# only json(jsonify) NOT render template or any use of Jinja!!

## authintactions and acsess to certain data by user
## root the admin has all acsees
## local host the libriran also for evrything
## normal user only to book inventory and his own loans by id 

## tasks
### backend
# DB with sqlalchemy on mySQL  -  done
# flask setup on seperate backend files - done
# do logger with IP datetime  - done
# fix the models  - done
# do JWS with tokens for login and singup - done
# check axios implement in code -  
# do models with crud operations getter and setter - 
# run tests with flask_cors - 


# *consider changing flask to FastAPI if stuck*


### frontend
# build htmls ones for users and ones for employees - 
# do JS with all the nesccerery buttons and function - 
# do css - 
# run tests to make sure everything works - 
# toastify for error handling -


# Backend Enhancements:
# Error Handling Improvements

# Implement structured error handling for API endpoints.
# Add proper HTTP status codes and messages.
# Create a global error handler.
# Security Enhancements

# Validate incoming data to prevent SQL injection and XSS.
# Add rate limiting to protect against abuse.
# Implement password hashing (if handling authentication manually).
# Role-Based Access Control (RBAC)

# Define roles (admin, employee, user).
# Implement permission-based route protection.
# Logging Enhancements

# Store logs in rotating files to prevent excessive growth.
# Implement different log levels (INFO, DEBUG, ERROR).
# Add alerts for critical logs.






### db manager.py - delivery man from db
# this file is talking with DB everyone that wants to talk to db does it only from this MF
# there is gonna a method called get books thats gonna connect to db and return the info it got from db

### buisness layer.py - middle man
# this is the file that metavech between db manager.py and api.py
# there is gonna be a methos called get books you recieve data from db via dbmanager.py


### api.py - delivery man from front
# the only file that talks to frontend everyone talks to front with this MF
# its getting the request and return data from buisnesslayer.py


## new methods get students(/get/students)
# return buisness layer.py get students



# the goal of the backend is to return answers/responses
