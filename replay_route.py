@app.route("/replay")
@login_required
def replay_view():
    if current_user.role != "admin":
        abort(403)
    from flask import jsonify
    traces = Trace.query.all()
    return jsonify([{"coords_json": t.coords_json} for t in traces])