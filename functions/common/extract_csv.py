import csv
from io import StringIO
from dataclasses import dataclass
from datetime import date
from dataclasses_jsonschema import JsonSchemaMixin
from typing import Generator

from google.cloud import storage
from google.oauth2 import service_account

from .settings import GCP_Project, GCP_Storage


@dataclass
class CsvSinkFormat(JsonSchemaMixin):
    source_type: str
    source: str
    review_id: str
    rating: int
    date: str
    text: str


@dataclass
class CsvSourceFormat(JsonSchemaMixin):
    review_id: str
    rating: str
    date: str
    text: str

    @classmethod
    def from_dict_to_sink(cls, data: dict, file_name: str) -> CsvSinkFormat:
        source = cls.from_dict(data)
        return CsvSinkFormat(
            review_id=source.review_id,
            rating=int(source.rating),
            date=source.date,
            text=source.text,
            source_type="csv",
            source=file_name
        )


class CloudStorageLoader:
    def __enter__(self):
        credentials = service_account.Credentials.from_service_account_file(GCP_Project.CREDENTIALS_FILE_PATH.value)
        self._storage_client = storage.Client(credentials=credentials)
        self._bucket = self._storage_client.get_bucket(GCP_Storage.BUCKET_NAME.value)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    def load_csv_data(self, file_name: str) -> Generator[CsvSinkFormat, None, None]:
        blob = self._bucket.get_blob(file_name, client=self._storage_client)
        blob_io = StringIO(blob.download_as_string().decode('utf-8'))
        reader = csv.reader(blob_io)
        header = next(reader)
        for row in reader:
            yield CsvSourceFormat.from_dict_to_sink(dict(zip(header, row)), file_name=file_name)
