from flask import Blueprint, render_template, redirect, url_for, abort, request, jsonify, current_app, send_file
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from models import db, User
import os
import shutil

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

def require_admin():
    if not (hasattr(current_user, "role") and current_user.role == "admin"):
        abort(403)

@admin_bp.get("/")
@login_required
def admin_root():
    require_admin()
    return redirect(url_for("admin.stops_page"))

@admin_bp.get("/stops")
@login_required
def stops_page():
    require_admin()
    return render_template("admin_stops.html")

@admin_bp.get("/users")
@login_required
def users_page():
    require_admin()
    return render_template("admin_users.html")

# ---- Users API (DB-backed) ----
@admin_bp.get("/api/users")
@login_required
def list_users():
    require_admin()
    users = db.session.query(User).order_by(User.role.desc(), User.username.asc()).all()
    return jsonify([{"username": u.username, "role": u.role} for u in users])

@admin_bp.post("/api/users")
@login_required
def create_user():
    require_admin()
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip().lower()
    role = (data.get("role") or "").strip().lower()
    password = data.get("password") or ""
    if not username or role not in {"carrier","substitute","admin"} or not password:
        return jsonify({"error": "Invalid payload"}), 400
    existing = db.session.query(User).filter_by(username=username).first()
    if existing:
        return jsonify({"error": "User exists"}), 409
    u = User(username=username, role=role, password_hash=generate_password_hash(password))
    db.session.add(u)
    db.session.commit()
    return jsonify({"ok": True, "username": u.username, "role": u.role})

@admin_bp.post("/api/users/<username>/password")
@login_required
def reset_password(username):
    require_admin()
    if hasattr(current_user, "username") and current_user.username == username:
        return jsonify({"error": "Cannot change your own password here"}), 400
    data = request.get_json(silent=True) or {}
    password = data.get("password") or ""
    if not password:
        return jsonify({"error": "Password required"}), 400
    u = db.session.query(User).filter_by(username=username).first()
    if not u:
        return jsonify({"error": "User not found"}), 404
    u.password_hash = generate_password_hash(password)
    db.session.commit()
    return jsonify({"ok": True})

@admin_bp.post("/api/users/<username>/role")
@login_required
def set_role(username):
    require_admin()
    if hasattr(current_user, "username") and current_user.username == username:
        return jsonify({"error": "Cannot change your own role here"}), 400
    u = db.session.query(User).filter_by(username=username).first()
    if not u:
        return jsonify({"error": "User not found"}), 404
    role = (request.get_json(silent=True) or {}).get("role", "").strip().lower()
    if role not in {"carrier", "substitute", "admin"}:
        return jsonify({"error": "Invalid role"}), 400
    u.role = role
    db.session.commit()
    return jsonify({"ok": True, "username": u.username, "role": u.role})

@admin_bp.delete("/api/users/<username>")
@login_required
def delete_user(username):
    require_admin()
    if hasattr(current_user, "username") and current_user.username == username:
        return jsonify({"error": "Cannot delete yourself"}), 400
    u = db.session.query(User).filter_by(username=username).first()
    if not u:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(u)
    db.session.commit()
    return jsonify({"ok": True})

# ---- DB Tools (admin only) ----

def _sqlite_path():
    uri = current_app.config.get("SQLALCHEMY_DATABASE_URI", "")
    if uri.startswith("sqlite:///"):
        p = uri.replace("sqlite:///", "", 1)
        if not os.path.isabs(p):
            p = os.path.join(os.getcwd(), p)
        return os.path.abspath(p)
    raise RuntimeError("Only sqlite:/// is supported for DB tools in this demo")

@admin_bp.get("/db/export")
@login_required
def db_export():
    require_admin()
    path = _sqlite_path()
    return send_file(path, as_attachment=True, download_name=os.path.basename(path))

@admin_bp.get("/db/backup")
@login_required
def db_backup():
    require_admin()
    path = _sqlite_path()
    backups_dir = os.path.join(os.path.dirname(path), "backups")
    os.makedirs(backups_dir, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    dst = os.path.join(backups_dir, f"db-{ts}.sqlite3")
    db.session.remove()
    try:
        engine = db.engine
    except Exception:
        engine = None
    if engine is not None:
        try:
            engine.dispose()
        except Exception:
            pass
    shutil.copy2(path, dst)
    return jsonify({"ok": True, "backup": os.path.basename(dst)})

@admin_bp.post("/db/import")
@login_required
def db_import():
    require_admin()
    if "file" not in request.files:
        return jsonify({"error": "No file"}), 400
    f = request.files["file"]
    filename = secure_filename(f.filename or "")
    if not filename.lower().endswith((".db", ".sqlite", ".sqlite3")):
        return jsonify({"error": "Provide a .db/.sqlite/.sqlite3 file"}), 400
    path = _sqlite_path()
    tmp = path + ".upload_tmp"
    f.save(tmp)
    db.session.remove()
    try:
        engine = db.engine
    except Exception:
        engine = None
    if engine is not None:
        try:
            engine.dispose()
        except Exception:
            pass
    shutil.move(tmp, path)
    return jsonify({"ok": True})
