# 🛡️ AuthGuard – Web Authentication Security

### A Flask-Based Web Authentication and Security Demonstration Project

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask-black.svg)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-blue.svg)](https://www.sqlite.org/)
[![Security](https://img.shields.io/badge/Focus-Web%20Security-green.svg)](https://owasp.org/)

---

## 📌 Project Overview

**AuthGuard – Web Authentication Security** is a Python Flask-based web application developed to demonstrate essential authentication and web application security mechanisms.

The project focuses on protecting user accounts against common authentication-related threats through password hashing, brute-force protection, temporary account lockout, CSRF validation, secure session management, and HTTP security headers.

AuthGuard provides an interactive environment where users can register, log in, access a personal security console, and observe security-related events.

It is developed as an educational Information Security mini project to understand how authentication mechanisms and security controls can be implemented in a web application.

## 🎯 Project Objectives

- To develop a secure user authentication system.
- To understand password hashing and password complexity validation.
- To prevent repeated unauthorized login attempts.
- To implement temporary account lockout against brute-force attempts.
- To protect forms using CSRF tokens.
- To understand secure session and cookie management.
- To implement HTTP security response headers.
- To maintain authentication and security event records.
- To demonstrate practical web application security concepts.

## ✨ Key Features

### 1. User Registration
- User account creation.
- Password complexity validation.
- Secure password storage using Werkzeug password hashing.

### 2. Secure Login Authentication
- Username and password verification.
- Password hash verification.
- Authentication session management.

### 3. Password Complexity Validation
The application enforces password requirements, including:
- Minimum 10 characters.
- At least one uppercase letter.
- At least one lowercase letter.
- At least one number.
- At least one special character.

### 4. Brute-Force Attack Protection
- Monitors repeated unsuccessful login attempts.
- Tracks login attempts for individual usernames.
- Temporarily locks an account after five failed attempts.
- Applies a two-minute lockout period for demonstration purposes.

### 5. CSRF Protection
- Generates CSRF tokens for POST forms.
- Validates submitted tokens to help prevent Cross-Site Request Forgery attacks.

### 6. Secure Session Management
- Uses Flask session management.
- Configures HttpOnly cookie protection.
- Configures SameSite cookie settings.

### 7. Security Event Logging
- Stores user and security-related events in SQLite.
- Helps demonstrate authentication activity and security monitoring.

### 8. HTTP Security Headers
Implements security response headers to improve browser-side protection and demonstrate secure web application configuration.

### 9. Personal Security Console
- Provides an authenticated area for users.
- Displays security-related information and recorded events.

### 10. Security Check
Provides a section for demonstrating the security response headers configured by the application.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| SQLite | Database management |
| HTML5 | Web page structure |
| CSS3 | User interface styling |
| JavaScript | Client-side functionality |
| Werkzeug | Password hashing and verification |
| Jinja2 | HTML templating |

## 🏗️ System Architecture

AuthGuard follows a simple client-server architecture.

1. **User Interface:** Users interact with the application through web pages.
2. **Flask Backend:** Processes registration, login, authentication, and security requests.
3. **Security Layer:** Performs password verification, CSRF validation, session handling, and login attempt monitoring.
4. **Database Layer:** SQLite stores user information and security events.
5. **Response Layer:** Flask returns the requested pages and configured HTTP security headers.

### Application Workflow

```text
             USER
               |
               v
       AUTHGUARD WEB APP
               |
               v
        FLASK BACKEND
               |
       +-------+-------+
       |               |
       v               v
   REGISTER          LOGIN
       |               |
       v               v
 PASSWORD           VERIFY
 VALIDATION         PASSWORD
       |               |
       v               v
 PASSWORD         LOGIN ATTEMPT
 HASHING           MONITORING
       |               |
       v               v
    SQLITE       AUTHENTICATION
    DATABASE          |
                      v
              SECURITY CONSOLE
                      |
                      v
              SECURITY EVENTS
```

## 📸 Project Screenshots

The following section presents the main interfaces of the AuthGuard application.

> Upload your actual project screenshots into a folder named `screenshots` in the GitHub repository. Use the filenames shown below or update the paths to match your uploaded images.

### 1. Home / Login Page

![AuthGuard Login Page](screenshots/login.png)

### 2. User Registration Page

![AuthGuard Registration Page](screenshots/register.png)

### 3. Personal Security Console

![AuthGuard Security Console](screenshots/dashboard.png)

### 4. Security Events

![AuthGuard Security Events](screenshots/security-logs.png)

### 5. Security Check

![AuthGuard Security Check](screenshots/security-check.png)

---

## 📂 Project Structure

```text
AuthGuard-Web-Authentication-Security/
│
├── app.py
│
├── authguard.db
│
├── requirements.txt
│
├── README.md
│
├── templates/
│   ├── HTML application templates
│
├── static/
│   ├── style.css
│   └── app.js
│
└── screenshots/
    ├── login.png
    ├── register.png
    ├── dashboard.png
    ├── security-logs.png
    └── security-check.png
```

## ⚙️ Installation and Setup

Follow these steps to run AuthGuard on a Windows computer.

### Prerequisites

- Python 3.10 or newer.
- Visual Studio Code (recommended).
- A modern web browser (Chrome or Microsoft Edge).

### Step 1: Clone the Repository

Open your terminal and execute:

```bash
git clone https://github.com/anubhaabhayan/AuthGuard-Web-Authentication-Security.git
```

### Step 2: Open the Project Folder

```bash
cd AuthGuard-Web-Authentication-Security
```

### Step 3: Create a Virtual Environment

```bash
py -m venv venv
```

### Step 4: Activate the Virtual Environment

```bash
venv\Scripts\activate
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Run the Application

```bash
python app.py
```

### Step 7: Open the Website

Open Chrome or Microsoft Edge and visit:

```text
http://127.0.0.1:5000
```

The AuthGuard application should now be accessible locally.

---

## 🧪 Project Demonstration

The following steps can be used to demonstrate the project during an academic presentation or practical examination.

1. Open the AuthGuard home page.
2. Explain the purpose of the authentication security application.
3. Register a new demonstration account.
4. Show the password complexity validation.
5. Log in using the registered credentials.
6. Open the personal security console.
7. Log out and attempt to log in using an incorrect password five times.
8. Demonstrate the temporary two-minute account lockout.
9. Log in again after the lockout expires.
10. Show the recorded security events.
11. Open the Security Check section and explain the configured HTTP security headers.

## 🔐 Security Considerations

AuthGuard demonstrates several important web authentication security concepts.

| Security Mechanism | Security Purpose |
|---|---|
| Password Hashing | Protects stored passwords |
| Password Validation | Enforces password complexity |
| Brute-Force Protection | Limits repeated failed login attempts |
| Account Lockout | Temporarily restricts repeated failed attempts |
| CSRF Validation | Protects POST forms against CSRF |
| Secure Cookies | Improves session cookie protection |
| Security Headers | Provides additional browser-side security |
| Event Logging | Records authentication and security events |

## ⚠️ Limitations

- The application is designed for local educational demonstration.
- It is not a complete enterprise authentication platform.
- The two-minute account lockout is intentionally short for classroom demonstration.
- The application does not perform external website vulnerability scanning.
- The built-in Flask development server is not intended for production deployment.

## 🚀 Future Enhancements

Possible improvements that can be considered in future versions include:

- Multi-factor authentication (MFA).
- Email-based account verification.
- Password reset functionality.
- CAPTCHA integration.
- Advanced rate limiting.
- Role-based access control.
- Enhanced security monitoring and reporting.
- Deployment using a production-ready web server.
- Automated security testing.

## 🎓 Project Information

**Project Name:** AuthGuard – Web Authentication Security

**Project Type:** Information Security Mini Project

**Domain:** Cybersecurity and Web Application Security

**Programming Language:** Python

**Framework:** Flask

**Database:** SQLite

**Development Environment:** Visual Studio Code

**Author:** Anubha Abhayan

## 📚 Learning Outcomes

Through this project, the following concepts can be understood and demonstrated:

- Practical implementation of authentication mechanisms.
- Password hashing and verification.
- Common authentication vulnerabilities.
- Brute-force attack prevention.
- CSRF protection.
- Session and cookie security.
- HTTP security headers.
- Database integration with Flask.
- Secure web application development.

## ⚠️ Disclaimer

This project is developed strictly for educational and demonstration purposes. It is intended to help understand authentication security mechanisms and basic web application protection.

Do not use real passwords or sensitive personal information while testing.

Before deploying the application publicly, configure a strong random `AUTHGUARD_SECRET`, enable HTTPS and `COOKIE_SECURE=1`, use a production server, and conduct an appropriate security review.

## 🔗 Repository

**GitHub:** https://github.com/anubhaabhayan/AuthGuard-Web-Authentication-Security

---

⭐ If you find this project useful for learning web authentication and security concepts, consider starring the repository.

**Developed by Anubha Abhayan**
