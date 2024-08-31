import requests
import json
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

base_url = os.environ["FLASK_URL"]
api_key = os.environ["FLASK_API_KEY"]

headers = {
    "FLASK-API-KEY": api_key
}
resp = requests.get(f"{base_url}/api/get_all", headers=headers)

if resp.status_code == 200:
    data = resp.json()
    data = [d for d in data if "prolific_id" in d and len(d["prolific_id"]) >= 20] 
    
    with open("data/raw/prolific_chatbot_data.json", "w") as f:
        json.dump(data, f, indent=2)
        