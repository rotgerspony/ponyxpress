# api_stops.py
from flask import Blueprint, request, jsonify, abort, Response
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from models import db, Stop

api_stops = Blueprint("api_stops", __name__, url_prefix="/api/stops")

def has_role(*roles):
    return (hasattr(current_user, "role") and current_user.role in roles)

def _parse_date(s):
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except Exception:
        return None

@api_stops.get("")
def list_stops():
    """
    Query params (all optional):
      label: substring match (case-insensitive)
      created_by: substring match (case-insensitive)
      date_from: YYYY-MM-DD (inclusive)
      date_to:   YYYY-MM-DD (inclusive)
      page:      1-based (default 1)
      page_size: default 25, max 200
    """
    q = Stop.query

    label = (request.args.get("label") or "").strip()
    created_by = (request.args.get("created_by") or "").strip()
    date_from = _parse_date(request.args.get("date_from"))
    date_to = _parse_date(request.args.get("date_to"))

    if label:
        q = q.filter(Stop.label.ilike(f"%{label}%"))
    if created_by:
        q = q.filter(Stop.created_by.ilike(f"%{created_by}%"))
    if date_from:
        q = q.filter(Stop.created_at >= datetime.combine(date_from, datetime.min.time()))
    if date_to:
        # inclusive end-of-day
        end = datetime.combine(date_to, datetime.min.time()) + timedelta(days=1)
        q = q.filter(Stop.created_at < end)

    q = q.order_by(Stop.id.desc())

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
            {"id": s.id, "label": s.label, "lng": s.lng, "lat": s.lat,
             "created_by": s.created_by, "created_at": s.created_at.isoformat()}
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

@api_stops.post("")
@login_required
def create_stop():
    if not has_role("carrier", "admin"):
        abort(403)
    data = request.get_json(silent=True) or {}
    try:
        lng = float(data.get("lng"))
        lat = float(data.get("lat"))
        label = (data.get("label") or "Mailbox").strip()[:120]
    except Exception:
        return jsonify({"error": "Invalid payload"}), 400
    s = Stop(label=label, lng=lng, lat=lat, created_by=getattr(current_user, "username", None))
    db.session.add(s)
    db.session.commit()
    return jsonify({"ok": True, "id": s.id}), 201

@api_stops.delete("/<int:stop_id>")
@login_required
def delete_stop(stop_id: int):
    if not has_role("admin"):
        abort(403)
    s = db.session.get(Stop, stop_id) or abort(404)
    db.session.delete(s)
    db.session.commit()
    return jsonify({"ok": True, "deleted": stop_id})

# Bulk delete (admin)
@api_stops.post("/bulk_delete")
@login_required
def bulk_delete():
    if not has_role("admin"):
        abort(403)
    data = request.get_json(silent=True) or {}
    ids = data.get("ids")
    if not isinstance(ids, list) or not ids:
        return jsonify({"error": "ids must be a non-empty list"}), 400
    try:
        ids_int = sorted({int(i) for i in ids})
    except Exception:
        return jsonify({"error": "ids must all be integers"}), 400

    rows = Stop.query.filter(Stop.id.in_(ids_int)).all()
    deleted = 0
    for s in rows:
        db.session.delete(s)
        deleted += 1
    db.session.commit()
    return jsonify({"ok": True, "deleted_count": deleted, "requested": len(ids_int)})

# Export all (admin)
@api_stops.get("/export")
@login_required
def export_stops():
    if not has_role("admin"):
        abort(403)
    import csv
    from io import StringIO
    rows = Stop.query.order_by(Stop.id.asc()).all()
    sio = StringIO()
    w = csv.writer(sio)
    w.writerow(["id", "label", "lng", "lat", "created_by", "created_at"])
    for s in rows:
        w.writerow([s.id, s.label, f"{s.lng:.6f}", f"{s.lat:.6f}", s.created_by or "", s.created_at.isoformat()])
    out = sio.getvalue()
    return Response(out, mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=stops.csv"})

# Export single stop (admin)
@api_stops.get("/<int:stop_id>/export")
@login_required
def export_single(stop_id: int):
    if not has_role("admin"):
        abort(403)
    import csv
    from io import StringIO
    s = db.session.get(Stop, stop_id) or abort(404)
    sio = StringIO()
    w = csv.writer(sio)
    w.writerow(["id", "label", "lng", "lat", "created_by", "created_at"])
    w.writerow([s.id, s.label, f"{s.lng:.6f}", f"{s.lat:.6f}", s.created_by or "", s.created_at.isoformat()])
    out = sio.getvalue()
    return Response(out, mimetype="text/csv",
                    headers={"Content-Disposition": f"attachment; filename=stop_{stop_id}.csv"})

