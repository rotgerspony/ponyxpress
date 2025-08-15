# ponyxpress_full_app.py — Final integrated version
import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ponyxpress.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    role = db.Column(db.String(20), default='carrier')

class Stop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    side = db.Column(db.String(10), default='right')
    user_id = db.Column(db.Integer)

class Trace(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coords_json = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer)

class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String(100))
    size = db.Column(db.String(20))
    destination = db.Column(db.String(120))
    photo_filename = db.Column(db.String(255))
    scanned_by = db.Column(db.Integer)
    scanned_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    return redirect(url_for("dashboard") if current_user.is_authenticated else url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"]).first()
        if user and user.password == request.form["password"]:
            login_user(user)
            return redirect(url_for("dashboard"))
        flash("Invalid login")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = User(email=request.form["email"], password=request.form["password"])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/scan", methods=["GET", "POST"])
@login_required
def scan():
    if request.method == "POST":
        file = request.files.get("photo")
        filename = None
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        pkg = Package(
            barcode=request.form.get("barcode"),
            size=request.form.get("size"),
            destination=request.form.get("destination"),
            photo_filename=filename,
            scanned_by=current_user.id
        )
        db.session.add(pkg)
        db.session.commit()
        return redirect(url_for("dashboard"))
    return render_template("scan.html")

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/map")
@login_required
def map_view():
    stops = Stop.query.filter_by(user_id=current_user.id).all()
    return render_template("map.html", stops=stops)

@app.route("/stops", methods=["POST"])
@login_required
def add_stop():
    data = request.get_json()
    stop = Stop(name=data.get("name"), lat=data.get("lat"), lng=data.get("lng"), side=data.get("side"), user_id=current_user.id)
    db.session.add(stop)
    db.session.commit()
    return jsonify({"status": "ok", "id": stop.id})

@app.route("/trace", methods=["POST"])
@login_required
def save_trace():
    coords = request.get_json().get("coords")
    trace = Trace(coords_json=str(coords), user_id=current_user.id)
    db.session.add(trace)
    db.session.commit()
    return jsonify({"status": "saved"})

@app.route("/replay")
@login_required
def replay_view():
    if current_user.role != "admin":
        abort(403)
    traces = Trace.query.all()
    return jsonify([{"coords_json": t.coords_json} for t in traces])

@app.route("/admin")
@login_required
def admin():
    if current_user.role != "admin":
        abort(403)
    return render_template("admin_dashboard.html")

@app.route("/admin/users")
@login_required
def admin_users():
    if current_user.role != "admin":
        abort(403)
    users = User.query.all()
    return render_template("admin_users.html", users=users)

@app.route("/admin/packages")
@login_required
def admin_packages():
    if current_user.role != "admin":
        abort(403)
    pkgs = Package.query.all()
    return render_template("admin_packages.html", pkgs=pkgs)

@app.route("/admin/stats")
@login_required
def admin_stats():
    if current_user.role != "admin":
        abort(403)
    return jsonify({
        "users": User.query.count(),
        "packages": Package.query.count(),
        "traces": Trace.query.count()
    })

@app.route("/admin/export")
@login_required
def admin_export():
    if current_user.role != "admin":
        abort(403)
    import csv
    from io import StringIO
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Barcode', 'Size', 'Destination'])
    for pkg in Package.query.all():
        writer.writerow([pkg.id, pkg.barcode, pkg.size, pkg.destination])
    return (
        output.getvalue(),
        200,
        {
            "Content-Type": "text/csv",
            "Content-Disposition": "attachment; filename=packages.csv"
        },
    )

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
