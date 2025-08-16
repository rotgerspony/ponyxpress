from app import app
from auth import reset_users

def login(client, username="alice", password="password"):
    return client.post("/login", data={"username": username, "password": password}, follow_redirects=True)

def test_save_requires_carrier_or_admin():
    c = app.test_client()
    reset_users()

    # not logged in -> 302/401/403 depending on login manager
    r = c.post("/api/stops", json={"lng": -94.49, "lat": 44.72, "label": "X"})
    assert r.status_code in (302, 401, 403)

    # substitute -> 403
    c.post("/logout", follow_redirects=True)
    login(c, "bob")  # bob is substitute by default after reset
    r = c.post("/api/stops", json={"lng": -94.49, "lat": 44.72, "label": "X"})
    assert r.status_code == 403

def test_save_as_carrier_and_delete_admin_only():
    c = app.test_client()
    reset_users()

    login(c, "alice")  # carrier
    r = c.post("/api/stops", json={"lng": -94.49, "lat": 44.72, "label": "Carrier Save"})
    assert r.status_code == 201
    stop_id = r.get_json()["id"]

    # carrier cannot delete
    r = c.delete(f"/api/stops/{stop_id}")
    assert r.status_code == 403

    # admin can delete
    c.post("/logout", follow_redirects=True)
    login(c, "admin")
    r = c.delete(f"/api/stops/{stop_id}")
    assert r.status_code == 200
