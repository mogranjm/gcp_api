from google.cloud import storage

from pygoodwe import SingleInverter
from .src.config import INVERTER_ID, INVERTER_USER, INVERTER_PASS

from src.config import INVERTER_ID, INVERTER_USER, INVERTER_PASS, GCS_BUCKET, GCS_KEY_PATH

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )


def main():
    inv = SingleInverter(INVERTER_ID, INVERTER_USER, INVERTER_PASS)

    current_output_kw = inv.data['inverter']['output_power'] / 1000
    total_production_today = inv.data['inverter']['eday']
