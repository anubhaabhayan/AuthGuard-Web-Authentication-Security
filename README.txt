AUTHGUARD - MCA INFORMATION SECURITY MINI PROJECT
=================================================

WHAT THIS PROJECT DOES
A local educational authentication security lab. It demonstrates:
- Registration and password complexity validation
- Password hashing (Werkzeug)
- Login attempt monitoring and temporary account lockout
- CSRF tokens on POST forms
- Session cookie settings (HttpOnly, SameSite)
- Security response headers
- SQLite-based user and event storage

RUN ON WINDOWS
1. Install Python 3.10 or newer.
2. Extract this ZIP folder.
3. Open the extracted folder in VS Code.
4. Open Terminal > New Terminal.
5. (Recommended) Create and activate a virtual environment:

   py -m venv venv
   venv\Scripts\activate

6. Install dependencies:

   pip install -r requirements.txt

7. Start the website:

   python app.py

8. Open this address in Chrome or Edge:

   http://127.0.0.1:5000

DEMO STEPS FOR YOUR TEACHER
1. Open the home page and explain the project objective.
2. Create a demo account. Password rule: 10+ characters, uppercase,
   lowercase, number and special character.
3. Sign in and show the personal security console.
4. Sign out. Try an incorrect password 5 times for that username.
   The account will be temporarily locked for 2 minutes.
5. Sign in after the lockout expires and show the recorded events.
6. Open Security Check to explain the configured response headers.

IMPORTANT NOTES
- This is a local classroom demonstration. It does not scan external sites.
- Use only test credentials. Do not use a personal or reused password.
- The two-minute lockout is intentionally short for a classroom demo.
- Before public deployment, set a strong random AUTHGUARD_SECRET environment
  variable, enable HTTPS and COOKIE_SECURE=1, use a production server,
  review rate limiting and account recovery, and perform a security review.
- The built-in development server is for local demonstration only.

PROJECT FILES
app.py                 Flask backend and SQLite database logic
templates/             HTML pages
static/style.css       Website styling
static/app.js          Password strength indicator
requirements.txt       Python dependency list
