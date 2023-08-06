import json

from google.cloud.storage import Client
from google.oauth2.service_account import Credentials

from koala_task_manager.writers.base_writer import BaseWriter


class GoogleStorageWriter(BaseWriter):
    def __init__(self, google_creds: dict, bucket_name: str, file_name: str):
        super().__init__(name="gcs_writer")
        self._client = self._create_client(credentials=google_creds)
        self._bucket_name = bucket_name
        self._file_name = file_name

    def write(self, report: dict) -> None:
        bucket = self._client.get_bucket(self._bucket_name)
        blob = bucket.get_blob(self._file_name)
        blob.upload_from_string(json.dumps(report))

    @staticmethod
    def _create_client(credentials: dict) -> Client:
        creds = Credentials.from_service_account_info(credentials)
        return Client(credentials=creds, project=creds.project_id)
