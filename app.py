import os
import re
import hmac
import secrets
import sqlite3
from datetime import datetime, timedelta, timezone
from functools import wraps
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "authguard.db"

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get("AUTHGUARD_SECRET", "dev-only-change-this-secret-before-deployment"),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("COOKIE_SECURE", "0") == "1",
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=20),
)

MAX_ATTEMPTS = 5
LOCK_MINUTES = 2  # Short demo lockout; use a longer policy in production.


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    with sqlite3.connect(DB_PATH) as db:
        db.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL,
            failed_attempts INTEGER NOT NULL DEFAULT 0,
            locked_until TEXT
        )""")
        db.execute("""CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            event_type TEXT NOT NULL,
            details TEXT NOT NULL,
            created_at TEXT NOT NULL
        )""")
        db.commit()


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def log_event(username, event_type, details):
    db = get_db()
    db.execute(
        "INSERT INTO events(username,event_type,details,created_at) VALUES(?,?,?,?)",
        (username, event_type, details, now_iso()),
    )
    db.commit()


def csrf_token():
    if "_csrf" not in session:
        session["_csrf"] = secrets.token_urlsafe(32)
    return session["_csrf"]


@app.context_processor
def inject_globals():
    return {"csrf_token": csrf_token, "current_user": session.get("username")}


@app.before_request
def protect_post_requests():
    if request.method == "POST":
        sent = request.form.get("_csrf", "")
        expected = session.get("_csrf", "")
        if not sent or not expected or not hmac.compare_digest(sent, expected):
            return render_template("message.html", title="Request blocked", message="The security token was missing or invalid. Refresh the page and try again."), 400


@app.after_request
def security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; style-src 'self' 'unsafe-inline'; "
        "script-src 'self' 'unsafe-inline'; img-src 'self' data:; "
        "font-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'"
    )
    response.headers["Cache-Control"] = "no-store"
    return response


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please sign in to open the security console.", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


def valid_password(password):
    return (
        len(password) >= 10
        and re.search(r"[A-Z]", password)
        and re.search(r"[a-z]", password)
        and re.search(r"\d", password)
        and re.search(r"[^A-Za-z0-9]", password)
    )


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not re.fullmatch(r"[A-Za-z0-9_]{3,24}", username):
            flash("Username must be 3–24 characters and use letters, numbers or underscore.", "danger")
            return render_template("register.html")
        if not valid_password(password):
            flash("Use at least 10 characters with uppercase, lowercase, a number and a symbol.", "danger")
            return render_template("register.html")
        db = get_db()
        try:
            db.execute(
                "INSERT INTO users(username,password_hash,created_at) VALUES(?,?,?)",
                (username, generate_password_hash(password), now_iso()),
            )
            db.commit()
        except sqlite3.IntegrityError:
            flash("That username is already registered. Choose another.", "danger")
            return render_template("register.html")
        log_event(username, "ACCOUNT_CREATED", "New account registered successfully.")
        flash("Account created. You can now sign in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()

        # Same generic error avoids revealing whether a username exists.
        if user:
            if user["locked_until"]:
                lock_time = datetime.fromisoformat(user["locked_until"])
                if datetime.now(timezone.utc) < lock_time:
                    log_event(username, "LOGIN_BLOCKED", "Attempt during temporary lockout.")
                    flash("Sign-in temporarily paused after repeated failures. Please wait two minutes.", "danger")
                    return render_template("login.html")
                db.execute("UPDATE users SET failed_attempts=0, locked_until=NULL WHERE id=?", (user["id"],))
                db.commit()

            if check_password_hash(user["password_hash"], password):
                db.execute("UPDATE users SET failed_attempts=0, locked_until=NULL WHERE id=?", (user["id"],))
                db.commit()
                session.clear()
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                session.permanent = True
                log_event(username, "LOGIN_SUCCESS", "Successful sign-in.")
                return redirect(url_for("dashboard"))

            attempts = user["failed_attempts"] + 1
            locked_until = None
            if attempts >= MAX_ATTEMPTS:
                locked_until = (datetime.now(timezone.utc) + timedelta(minutes=LOCK_MINUTES)).isoformat(timespec="seconds")
                attempts = 0
            db.execute("UPDATE users SET failed_attempts=?, locked_until=? WHERE id=?",
                       (attempts, locked_until, user["id"]))
            db.commit()
        log_event(username or "unknown", "LOGIN_FAILURE", "Invalid sign-in attempt.")
        flash("Sign-in failed. Check your details or wait if the account is temporarily locked.", "danger")
    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    db = get_db()
    events = db.execute(
        "SELECT event_type, details, created_at FROM events WHERE username=? ORDER BY id DESC LIMIT 8",
        (session["username"],),
    ).fetchall()
    stats = db.execute(
        "SELECT COUNT(*) AS total, SUM(CASE WHEN event_type='LOGIN_FAILURE' THEN 1 ELSE 0 END) AS failures "
        "FROM events WHERE username=?", (session["username"],)
    ).fetchone()
    return render_template("dashboard.html", events=events, stats=stats)


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    username = session.get("username", "unknown")
    log_event(username, "LOGOUT", "User signed out.")
    session.clear()
    flash("You have signed out securely.", "success")
    return redirect(url_for("home"))


@app.route("/security-check")
def security_check():
    # Shows headers configured by this application, not a scan of another site.
    checks = [
        ("X-Content-Type-Options", "nosniff", "Helps prevent MIME-type sniffing."),
        ("X-Frame-Options", "DENY", "Helps prevent the page being embedded in a frame."),
        ("Referrer-Policy", "strict-origin-when-cross-origin", "Limits referrer information sent to other sites."),
        ("Content-Security-Policy", "default-src 'self'", "Restricts where page resources may load from."),
        ("HttpOnly session cookie", "Enabled", "Helps prevent client-side scripts from reading the session cookie."),
        ("SameSite session cookie", "Lax", "Reduces some cross-site request risks."),
    ]
    return render_template("security_check.html", checks=checks)


@app.route("/about")
def about():
    return render_template("about.html")


@app.errorhandler(404)
def not_found(error):
    return render_template("message.html", title="Page not found", message="The page you requested does not exist."), 404


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=False)
