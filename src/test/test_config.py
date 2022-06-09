from unittest import TestCase
from pygoodwe import SingleInverter
from google.cloud import storage

from ..config import INVERTER_ID, INVERTER_USER, INVERTER_PASS, GCS_BUCKET, GCS_KEY_PATH


class TestConfig(TestCase):

    def test_load_dotenv(self):
        # 5 Environment variables configured
        self.assertIsNotNone(INVERTER_ID)
        self.assertIsNotNone(INVERTER_USER)
        self.assertIsNotNone(INVERTER_PASS)
        self.assertIsNotNone(GCS_KEY_PATH)
        self.assertIsNotNone(GCS_BUCKET)

    def test_get_inverter_data(self):
        inv = SingleInverter(INVERTER_ID, INVERTER_USER, INVERTER_PASS, skipload=True)
        data = inv.getCurrentReadings()
        self.assertIsNotNone(data)

    def test_gcs_bucket(self):
        client = storage.Client.from_service_account_json(GCS_KEY_PATH)
        buckets = list(client.list_buckets())
        self.assertIn(buckets, GCS_BUCKET)
