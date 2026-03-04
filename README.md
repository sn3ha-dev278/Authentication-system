# Secure Authentication System (Flask)

This project is a simple authentication system built with Flask that focuses on implementing basic security controls commonly used in real-world web applications. The goal of this project was to understand how authentication mechanisms work and how common attacks against login systems can be mitigated.

The application allows users to register, log in, and access a protected dashboard. Along with the basic functionality, several security measures have been implemented to make the system more resilient against common web attacks.

---

## Features

* User registration and login system
* Password hashing using bcrypt
* Session-based authentication
* Protected dashboard route
* Rate limiting on login attempts
* CSRF protection in forms
* SQL injection mitigation using ORM queries
* Logout functionality

---

## Security Controls Implemented

### Password Hashing

User passwords are never stored in plaintext. Passwords are hashed using bcrypt before being saved in the database.

### Rate Limiting

Login attempts are limited to prevent brute-force attacks. If a user sends too many login requests within a short period of time, the server blocks further attempts temporarily.

### CSRF Protection

All forms are protected using CSRF tokens through Flask-WTF. Requests without a valid CSRF token are rejected.

### SQL Injection Mitigation

The application uses SQLAlchemy ORM to interact with the database. Since user input is never directly concatenated into SQL queries, parameterized queries are automatically used to prevent SQL injection.

### Authentication Sessions

Flask-Login is used to manage user sessions. Only authenticated users can access the dashboard route.

---

## Project Structure

```
AuthenticationSystem
│
├── app.py
├── database.db
│
├── templates
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── rate_limit.html
│
└── static
```

---

## Technologies Used

* Python
* Flask
* Flask-Login
* Flask-WTF
* Flask-Limiter
* SQLAlchemy
* SQLite
* bcrypt

---

## Running the Project

Clone the repository and install the dependencies.

```
pip install flask flask_sqlalchemy flask_login flask_wtf flask_bcrypt flask_limiter
```

Run the application:

```
python app.py
```

The server will start on:

```
http://127.0.0.1:5000
```

---

## Security Testing

Some basic tests were performed against the login system to verify the implemented protections.

Example SQL injection payloads tested:

```
' OR 1=1 --
admin' --
' UNION SELECT 1,2,3 --
```

Result:
Authentication bypass was not possible because SQLAlchemy uses parameterized queries.

Rate limiting was also tested by repeatedly sending login requests. After exceeding the allowed limit, the server returned an HTTP 429 response.

---

## Notes

The focus was on understanding how authentication systems work and how common vulnerabilities can be mitigated at the application level.
While the system includes certain security controls, it is still a simplified example and not intended for production use.

---

## Possible Improvements

Some features that could be added in the future:

* Account lockout after multiple failed login attempts
* Login attempt logging and monitoring
* Password strength validation
* Email verification for new users
* Two-factor authentication (2FA)

---
