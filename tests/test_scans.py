from app import app
from auth import reset_users

def login(c, u, p="password"):
    return c.post("/login", data={"username": u, "password": p}, follow_redirects=True)

def test_scans_permissions_and_create_list():
    c = app.test_client()
    reset_users()

    # not logged in -> cannot list or create
    r = c.get("/api/scans")
    assert r.status_code in (302, 401, 403)

    login(c, "bob")  # substitute
    # list allowed for logged-in substitute
    r = c.get("/api/scans")
    assert r.status_code == 200
    # create should be forbidden for substitute
    r = c.post("/api/scans", json={"code":"X","size":"small","destination":"mailbox"})
    assert r.status_code == 403

    c.post("/logout", follow_redirects=True)
    login(c, "alice")  # carrier
    # create ok
    r = c.post("/api/scans", json={"code":"ABC123","size":"small","destination":"mailbox","lng":-94.49,"lat":44.72})
    assert r.status_code == 201
    scan_id = r.get_json()["id"]

    # list returns our scan with meta
    r = c.get("/api/scans")
    j = r.get_json()
    assert "items" in j and "meta" in j
    assert any(it["id"] == scan_id for it in j["items"])

    # admin can delete
    c.post("/logout", follow_redirects=True)
    login(c, "admin")
    r = c.delete(f"/api/scans/{scan_id}")
    assert r.status_code == 200
