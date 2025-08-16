from app import app
from auth import reset_users

def login(c, u, p="password"):
    return c.post("/login", data={"username": u, "password": p}, follow_redirects=True)

def test_list_then_create_and_list():
    c = app.test_client()
    reset_users()

    # list with metadata
    r = c.get("/api/stops")
    assert r.status_code == 200
    data = r.get_json()
    assert isinstance(data, dict) and "items" in data and "meta" in data
    start_total = data["meta"]["total"]

    # create one as carrier
    login(c, "alice")
    r = c.post("/api/stops", json={"lng": -94.49, "lat": 44.72, "label": "Mailbox Test"})
    assert r.status_code == 201

    # total increases by 1
    r = c.get("/api/stops")
    data2 = r.get_json()
    assert data2["meta"]["total"] == start_total + 1
