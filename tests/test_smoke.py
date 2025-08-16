from app import app

def test_healthcheck():
    c = app.test_client()
    r = c.get("/healthz")
    assert r.status_code == 200
