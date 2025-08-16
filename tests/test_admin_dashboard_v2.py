from app import app

def login(c, u, p="password"):
    return c.post("/login", data={"username": u, "password": p}, follow_redirects=True)

def test_filters_and_pagination():
    c = app.test_client()
    login(c, "alice")
    # seed 30 stops
    for i in range(30):
        c.post("/api/stops", json={"lng": -94.49 + i*0.0001, "lat": 44.72, "label": f"Box {i}"})
    # filter by label contains "Box 2"
    r = c.get("/api/stops?label=Box 2&page=1&page_size=10")
    j = r.get_json(); assert r.status_code == 200
    assert j["meta"]["page"] == 1
    assert any("Box 2" in it["label"] for it in j["items"])
    # pagination sanity
    r = c.get("/api/stops?page=2&page_size=10")
    j = r.get_json(); assert j["meta"]["page"] == 2

def test_export_single_requires_admin():
    c = app.test_client()
    login(c, "alice")
    r = c.post("/api/stops", json={"lng": -94.5, "lat": 44.7, "label": "one"})
    sid = r.get_json()["id"]
    # carrier cannot export single
    r = c.get(f"/api/stops/{sid}/export"); assert r.status_code == 403
    # admin can
    c.post("/logout", follow_redirects=True)
    login(c, "admin")
    r = c.get(f"/api/stops/{sid}/export")
    assert r.status_code == 200
    assert r.mimetype == "text/csv"

def test_user_role_api_admin_only_and_no_self_edit():
    c = app.test_client()
    login(c, "bob")  # substitute
    r = c.get("/admin/api/users"); assert r.status_code == 403
    c.post("/logout", follow_redirects=True)
    login(c, "admin")
    r = c.get("/admin/api/users"); assert r.status_code == 200
    # cannot change own role
    r = c.post("/admin/api/users/admin/role", json={"role": "carrier"})
    assert r.status_code == 400
    # can change others
    r = c.post("/admin/api/users/bob/role", json={"role": "carrier"})
    assert r.status_code == 200
