# api_scans.py
from flask import Blueprint, request, jsonify, abort
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from models import db, Scan

api_scans = Blueprint("api_scans", __name__, url_prefix="/api/scans")

def has_role(*roles):
    return (hasattr(current_user, "role") and current_user.role in roles)

def _parse_date(s):
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except Exception:
        return None

@api_scans.get("")
@login_required
def list_scans():
    """
    Query params (optional): code, created_by, date_from, date_to (YYYY-MM-DD), page, page_size
    """
    q = Scan.query
    code = (request.args.get("code") or "").strip()
    created_by = (request.args.get("created_by") or "").strip()
    date_from = _parse_date(request.args.get("date_from"))
    date_to = _parse_date(request.args.get("date_to"))

    if code:
        q = q.filter(Scan.code.ilike(f"%{code}%"))
    if created_by:
        q = q.filter(Scan.created_by.ilike(f"%{created_by}%"))
    if date_from:
        q = q.filter(Scan.created_at >= datetime.combine(date_from, datetime.min.time()))
    if date_to:
        end = datetime.combine(date_to, datetime.min.time()) + timedelta(days=1)
        q = q.filter(Scan.created_at < end)

    q = q.order_by(Scan.id.desc())
    try:
        page = max(int(request.args.get("page", 1)), 1)
    except Exception:
        page = 1
    try:
        page_size = int(request.args.get("page_size", 25))
    except Exception:
        page_size = 25
    page_size = max(1, min(page_size, 200))

    total = q.count()
    items = q.offset((page - 1) * page_size).limit(page_size).all()

    return jsonify({
        "items": [
            {"id": s.id, "code": s.code, "size": s.size, "destination": s.destination,
             "lng": s.lng, "lat": s.lat, "created_by": s.created_by, "created_at": s.created_at.isoformat()}
            for s in items
        ],
        "meta": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": (total + page_size - 1) // page_size,
            "has_next": page * page_size < total,
            "has_prev": page > 1
        }
    })

@api_scans.post("")
@login_required
def create_scan():
    if not has_role("carrier", "admin"):
        abort(403)
    data = request.get_json(silent=True) or {}
    code = (data.get("code") or "").strip()
    size = (data.get("size") or "").strip().lower()
    destination = (data.get("destination") or "").strip().lower()
    if not code or size not in {"small","large"} or destination not in {"mailbox","house"}:
        return jsonify({"error": "Invalid payload"}), 400
    lng = data.get("lng"); lat = data.get("lat")
    try:
        lng = float(lng) if lng is not None else None
        lat = float(lat) if lat is not None else None
    except Exception:
        return jsonify({"error": "Invalid coordinates"}), 400

    s = Scan(code=code, size=size, destination=destination, lng=lng, lat=lat,
             created_by=getattr(current_user, "username", None))
    db.session.add(s)
    db.session.commit()
    return jsonify({"ok": True, "id": s.id}), 201

@api_scans.delete("/<int:scan_id>")
@login_required
def delete_scan(scan_id: int):
    if not has_role("admin"):
        abort(403)
    s = db.session.get(Scan, scan_id) or abort(404)
    db.session.delete(s)
    db.session.commit()
    return jsonify({"ok": True, "deleted": scan_id})

