from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
import secrets
from models import db as db

bp = Blueprint("shipments", __name__, url_prefix="/shipments")

class Shipment(db.Model):
    __tablename__ = "shipments"
    id = db.Column(db.Integer, primary_key=True)
    tracking_code = db.Column(db.String(12), unique=True, nullable=False, index=True)
    customer_name = db.Column(db.String(120), nullable=False)
    pickup_address = db.Column(db.String(255), nullable=False)
    dropoff_address = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(32), nullable=False, default="CREATED")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

def _new_tracking():
    return secrets.token_hex(4).upper()

@bp.route("/")
@login_required
def index():
    shipments = Shipment.query.order_by(Shipment.created_at.desc()).all()
    return render_template("shipments/index.html", shipments=shipments)

@bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    if request.method == "POST":
        s = Shipment(
            tracking_code=_new_tracking(),
            customer_name=request.form["customer_name"].strip(),
            pickup_address=request.form["pickup_address"].strip(),
            dropoff_address=request.form["dropoff_address"].strip(),
        )
        db.session.add(s)
        db.session.commit()
        flash(f"Shipment created: {s.tracking_code}", "success")
        return redirect(url_for("shipments.show", tracking=s.tracking_code))
    return render_template("shipments/new.html")

@bp.route("/<tracking>")
@login_required
def show(tracking):
    s = Shipment.query.filter_by(tracking_code=tracking).first_or_404()
    return render_template("shipments/show.html", s=s)

# Public tracker (no login)
@bp.route("/t/<tracking>")
def public(tracking):
    s = Shipment.query.filter_by(tracking_code=tracking).first_or_404()
    return render_template("shipments/track.html", s=s)

# Tiny JSON API
@bp.route("/api", methods=["POST"])
def api_create():
    data = request.get_json(force=True)
    s = Shipment(
        tracking_code=_new_tracking(),
        customer_name=data["customer_name"],
        pickup_address=data["pickup_address"],
        dropoff_address=data["dropoff_address"],
    )
    db.session.add(s)
    db.session.commit()
    return jsonify({"tracking_code": s.tracking_code, "status": s.status}), 201

@bp.route("/api/<tracking>")
def api_get(tracking):
    s = Shipment.query.filter_by(tracking_code=tracking).first_or_404()
    return jsonify({
        "tracking_code": s.tracking_code,
        "status": s.status,
        "customer_name": s.customer_name,
        "pickup_address": s.pickup_address,
        "dropoff_address": s.dropoff_address,
        "created_at": s.created_at.isoformat()
    })