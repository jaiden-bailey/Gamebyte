# Gamebyte

# Flask Web Application

This Flask web application provides a basic user authentication system, allowing users to register, login, and access protected pages. It uses Flask, Flask-Login, Flask-Session, Flask-SQLAlchemy, and Werkzeug for security.

## Features

- User registration and login
- Password hashing
- Session management
- Protected routes that require authentication
- SQLite database integration

## Installation

1. Clone the repository:
2.  Install the required packages:
   
   ## Configuration

- Set the `SECRET_KEY` in the application to a strong secret value.
- Configure the `SQLALCHEMY_DATABASE_URI` if you're not using SQLite or need a different database.

## Running the Application

1. Initialize the database:
