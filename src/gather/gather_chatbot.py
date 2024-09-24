import requests
import json
import os
from dotenv import load_dotenv
from pprint import pprint
import pandas as pd

load_dotenv()

base_url = os.environ["FLASK_URL"]
api_key = os.environ["FLASK_API_KEY"]

QUALTRICS_FILE = "data/proc/micronarrative_llm_vs_qualtrics_aug2024_proc.csv"

headers = {
    "FLASK-API-KEY": api_key
}

chatbot_data = []
df_qualtrics = pd.read_csv(QUALTRICS_FILE)
successes = 0
for i, pid in enumerate(df_qualtrics['pid'].values):
    if i % 10 == 0:
        print(f"Processing {i+1}/{len(df_qualtrics)}")
    resp = requests.post(f"{base_url}/api/get_pid", headers=headers, json={"prolific_id": pid})
    if resp.status_code == 200:
        chatbot_data += resp.json()
        successes += 1
    else:
        print(f"Failed to get chatbot data for {pid}")
        print("status code:", resp.status_code)
        print("text:", resp.text)
        continue
    if len(resp.json()) == 0:
        print(f"No chatbot data for {pid}")

unique_pids = set([d["prolific_id"] for d in chatbot_data])
print(f"Successfully retrieved {successes} records for {len(unique_pids)} unique Prolific IDs")

with open("data/raw/prolific_chatbot_data.json", "w") as f:
    json.dump(chatbot_data, f, indent=2)