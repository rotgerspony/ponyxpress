
import requests
ORS_API_KEY = "your-api-key-here"

def get_route(coords):
    url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"
    headers = {"Authorization": ORS_API_KEY}
    data = {
        "coordinates": coords
    }
    res = requests.post(url, json=data, headers=headers)
    return res.json() if res.status_code == 200 else {"error": res.text}
