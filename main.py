from google.cloud import storage
from datetime import date
from pygoodwe import SingleInverter
import pandas as pd

from src.config import INVERTER_ID, INVERTER_USER, INVERTER_PASS, GCS_BUCKET, GCS_KEY_PATH


def dataframe_to_storage_blob_as_csv(bucket_name, dataframe, destination_blob_filename):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name.csv"

    storage_client = storage.Client.from_service_account_json(GCS_KEY_PATH)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_filename)

    blob.upload_from_string(dataframe.to_csv(), 'text/csv')

    print(
        f"Data uploaded to {destination_blob_filename}."
    )


def get_current_solar_data():
    inv = SingleInverter(INVERTER_ID, INVERTER_USER, INVERTER_PASS)

    df = pd.DataFrame({
        'timestamp': [inv.data['inverter']['time']],
        'current_output_kw': [inv.data['inverter']['output_power']],
        'total_production_today': [inv.data['inverter']['eday']]
    })

    dataframe_to_storage_blob_as_csv(GCS_BUCKET, df, f"{date.today().strftime('%Y%m%d')}/inverter_log_{inv.data['inverter']['time']}")


if __name__ == "__main__":
    get_current_solar_data()
