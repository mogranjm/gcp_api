import json
from datetime import datetime

from google.cloud import storage
from pygoodwe import SingleInverter
from pytz import timezone

from src.config import INVERTER_ID, INVERTER_USER, INVERTER_PASS, GCS_BUCKET


def to_storage_bucket(bucket_name, data, destination_blob_filename):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name.csv"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_filename)

    blob.upload_from_string(data, 'application/json')

    print(
        f"Data uploaded to {destination_blob_filename}."
    )


def get_current_solar_data(event, context):
    inv = SingleInverter(INVERTER_ID, INVERTER_USER, INVERTER_PASS)

    # dump single inverter record to string (one line, ok for BigQuery)
    data = json.dumps(inv.data['inverter'])

    timestamp = datetime.strptime(inv.data['inverter']['time'], "%m/%d/%Y %H:%M:%S")
    timestamp = datetime.strftime(timestamp, "%Y%m%d %H:%M")

    to_storage_bucket(
        GCS_BUCKET,
        data,
        f"{datetime.now(timezone('Australia/Melbourne')).strftime('%Y%m%d')}/inverter_log_{timestamp}"  # default format includes '/' which messes with folder creation in blob storage}"
    )


if __name__ == "__main__":
    event = ''
    context = ''
    get_current_solar_data(event, context)
