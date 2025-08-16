from app import app

def test_map_buttons_present():
    c = app.test_client()
    r = c.get("/map")
    assert r.status_code == 200
    # Look for button labels
    assert b"Locate Me" in r.data
    assert b"Mailbox (Right of Travel)" in r.data
    assert b"Mailbox (Left of Travel)" in r.data
    assert b"Mailbox at Click" in r.data
