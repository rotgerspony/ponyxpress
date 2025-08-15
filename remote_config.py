
import json

def fetch_remote_config(path="config.json"):
    with open(path, "r") as f:
        return json.load(f)
