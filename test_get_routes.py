
import requests

BASE_URL = "http://127.0.0.1:5000"

routes = [
    "/", "/login", "/register", "/dashboard", "/scan", "/packages", 
    "/admin", "/logout", "/uploads/test.jpg"
]

def test_get_routes():
    print("Testing GET routes...")
    for route in routes:
        try:
            response = requests.get(BASE_URL + route)
            print(f"GET {route} -> {response.status_code}")
        except Exception as e:
            print(f"ERROR GET {route}: {e}")

if __name__ == "__main__":
    test_get_routes()
