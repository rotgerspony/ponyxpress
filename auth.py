from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from typing import Optional
from models import db, User

auth_bp = Blueprint("auth", __name__)

# Defaults: alice (carrier), bob (substitute), admin (admin). Password for all is "password".
_DEFAULT_PWD_HASH = generate_password_hash("password")
DEFAULT_USERS = [
    {"username": "alice", "role": "carrier",    "password_hash": _DEFAULT_PWD_HASH},
    {"username": "bob",   "role": "substitute", "password_hash": _DEFAULT_PWD_HASH},
    {"username": "admin", "role": "admin",      "password_hash": _DEFAULT_PWD_HASH},
]

def _resolve_app(app=None):
    """Return an app object, preferring provided arg, then current_app, then importing app.app."""
    if app is not None:
        return app
    try:
        return current_app._get_current_object()
    except Exception:
        # late import avoids circular import at module load time
        from app import app as flask_app
        return flask_app

def ensure_default_users(app=None):
    """Create default users if the users table is empty."""
    app = _resolve_app(app)
    with app.app_context():
        if db.session.query(User).count() == 0:
            for u in DEFAULT_USERS:
                db.session.add(User(username=u["username"], role=u["role"], password_hash=u["password_hash"]))
            db.session.commit()

def reset_users(app=None):
    """Reset users table to DEFAULT_USERS (used by tests). Safe without an active app context."""
    app = _resolve_app(app)
    with app.app_context():
        db.session.query(User).delete()
        for u in DEFAULT_USERS:
            db.session.add(User(username=u["username"], role=u["role"], password_hash=u["password_hash"]))
        db.session.commit()

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        @login_required
        def wrapper(*args, **kwargs):
            if not hasattr(current_user, "role") or current_user.role not in roles:
                abort(403)
            return f(*args, **kwargs)
        return wrapper
    return decorator

@auth_bp.get("/login")
def login_page():
    return render_template("login.html")

@auth_bp.post("/login")
def login_submit():
    username = (request.form.get("username") or "").strip().lower()
    password = request.form.get("password") or ""
    user: Optional[User] = db.session.query(User).filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        flash(f"Welcome, {username}!", "success")
        return redirect(url_for("home"))
    flash("Invalid credentials", "error")
    return redirect(url_for("auth.login_page"))

@auth_bp.post("/logout")
@login_required
def logout_submit():
    logout_user()
    flash("Logged out", "info")
    return redirect(url_for("home"))

def init_login_manager(app):
    lm = LoginManager(app)
    lm.login_view = "auth.login_page"

    @lm.user_loader
    def load_user(user_id: str):
        try:
            uid = int(user_id)
        except Exception:
            return None
        return db.session.get(User, uid)
    return lm
