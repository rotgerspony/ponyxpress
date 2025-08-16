# tests/test_auth.py
from app import app

def login(client, username="alice", password="password"):
    return client.post("/login", data={"username": username, "password": password}, follow_redirects=True)

def test_login_logout_cycle():
    c = app.test_client()
    r = login(c, "alice", "password")
    assert r.status_code == 200
    r = c.post("/logout", follow_redirects=True)
    assert r.status_code == 200

def test_role_gates():
    c = app.test_client()
    login(c, "alice", "password")  # role: carrier
    assert c.get("/carrier").status_code == 200
    assert c.get("/substitute").status_code == 403
    assert c.get("/admin").status_code == 403
