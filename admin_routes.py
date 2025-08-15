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
    return render_template_string("<h2>Users</h2>" + "".join([f"<li>{u.email} - {u.role}</li>" for u in users]))

@app.route("/admin/packages")
@login_required
def admin_packages():
    if current_user.role != "admin":
        abort(403)
    pkgs = Package.query.all()
    return render_template_string("<h2>All Packages</h2>" + "".join([f"<li>{p.barcode} - {p.destination}</li>" for p in pkgs]))

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
    return Response(output.getvalue(), mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=packages.csv"})

@app.route("/admin/stats")
@login_required
def admin_stats():
    if current_user.role != "admin":
        abort(403)
    from datetime import datetime
    total_users = User.query.count()
    total_packages = Package.query.count()
    return render_template_string(f"<h2>Stats</h2><ul><li>Total Users: {total_users}</li><li>Total Packages: {total_packages}</li></ul>")