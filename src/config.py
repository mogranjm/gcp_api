import json
import os

from dotenv import load_dotenv

config = load_dotenv("src/.env")

env = os.environ

INVERTER_ID = env.get("GOODWE_STATION_ID")
INVERTER_USER = env.get("GOODWE_USER")
INVERTER_PASS = env.get("GOODWE_PASSWORD")

GCS_BUCKET = env.get("GCS_BUCKET_NAME")
GCS_KEY_PATH = env.get("GCS_SERVICE_ACCOUNT_KEY")

# If service account creds not present in environment (they should be in prod), load them from local
if env.get("GOOGLE_APPLICATION_CREDENTIALS") is None:
    with open(GCS_KEY_PATH, 'r') as f:
        data = f.read()
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = json.loads(data)
