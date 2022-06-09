from dotenv import dotenv_values

config = dotenv_values("src/.env")

INVERTER_ID = config["GOODWE_STATION_ID"]
INVERTER_USER = config["GOODWE_USER"]
INVERTER_PASS = config["GOODWE_PASSWORD"]

GCS_BUCKET = config["GCS_BUCKET_NAME"]
GCS_KEY_PATH = config["GCS_SERVICE_ACCOUNT_KEY"]
