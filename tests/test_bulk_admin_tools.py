from app import app
from auth import reset_users

def login(client, username, password="password"):
    return client.post("/login", data={"username": username, "password": password}, follow_redirects=True)

def test_bulk_delete_requires_admin():
    c = app.test_client()
    reset_users()

    # create some stops as carrier
    login(c, "alice")
    ids = []
    for i in range(3):
        r = c.post("/api/stops", json={"lng": -94.49 + i*0.001, "lat": 44.72 + i*0.001, "label": f"S{i}"})
        assert r.status_code == 201
        ids.append(r.get_json()["id"])

    # try bulk delete as carrier -> 403
    r = c.post("/api/stops/bulk_delete", json={"ids": ids})
    assert r.status_code == 403

    # bulk delete as admin -> 200
    c.post("/logout", follow_redirects=True)
    login(c, "admin")
    r = c.post("/api/stops/bulk_delete", json={"ids": ids})
    assert r.status_code == 200
    data = r.get_json()
    assert data["deleted_count"] == len(ids)

    # list should not include those ids
    r = c.get("/api/stops")
    items = r.get_json()["items"]
    remaining_ids = {s["id"] for s in items}
    for id_ in ids:
        assert id_ not in remaining_ids
