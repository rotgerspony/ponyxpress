from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# ---- Persistent Users ----
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(32), nullable=False, default="substitute")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

# ---- Stops ----
class Stop(db.Model):
    __tablename__ = "stops"
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(120), nullable=False)
    lng = db.Column(db.Float, nullable=False)
    lat = db.Column(db.Float, nullable=False)
    created_by = db.Column(db.String(80), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

# ---- Scans ----
class Scan(db.Model):
    __tablename__ = "scans"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(256), nullable=False, index=True)
    size = db.Column(db.String(16), nullable=False)          # "small" or "large"
    destination = db.Column(db.String(32), nullable=False)   # "mailbox" or "house"
    lng = db.Column(db.Float, nullable=True)
    lat = db.Column(db.Float, nullable=True)
    created_by = db.Column(db.String(80), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
