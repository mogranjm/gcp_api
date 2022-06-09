from dotenv import dotenv_values

config = dotenv_values(".env")

INVERTER_ID = config["GOODWE_STATION_ID"]
INVERTER_USER = config["GOODWE_USER"]
INVERTER_PASS = config["GOODWE_PASSWORD"]
