import os

from dotenv import load_dotenv

config = load_dotenv("src/.env")

env = os.environ

INVERTER_ID = env.get("GOODWE_STATION_ID")
INVERTER_USER = env.get("GOODWE_USER")
INVERTER_PASS = env.get("GOODWE_PASSWORD")

GCS_BUCKET = env.get("GCS_BUCKET_NAME")
