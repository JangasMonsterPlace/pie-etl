import csv
from io import StringIO
from dataclasses import dataclass
from datetime import datetime
from dataclasses_jsonschema import JsonSchemaMixin
from typing import Generator, Optional

from google.cloud import storage

from .settings import GCP_Project, GCP_Storage


@dataclass
class CsvSinkFormat(JsonSchemaMixin):
    source_type: str
    source: str
    review_id: str
    rating: int
    date: str
    text: str
    group: Optional[str] = None
    user: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None


@dataclass
class CsvSourceFormat(JsonSchemaMixin):
    review_id: str
    rating: str
    date: str
    text: str
    user: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None

    @classmethod
    def from_dict_to_sink(cls, data: dict, file_name: str, date_format: str, group: str) -> CsvSinkFormat:
        source = cls.from_dict(data)
        date = datetime.strptime(source.date, date_format).strftime("%Y-%m-%d")
        return CsvSinkFormat(
            review_id=source.review_id,
            rating=int(source.rating),
            date=date,
            text=source.text,
            source_type="csv",
            source=file_name,
            group=group,
            city=source.city,
            country=source.country,
            user=source.user
        )


class CloudStorageLoader:
    def __enter__(self):
        self._storage_client = storage.Client(credentials=GCP_Project.CREDENTIALS.value)
        self._bucket = self._storage_client.get_bucket(GCP_Storage.BUCKET_NAME.value)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    def load_csv_data(self, file_name: str) -> Generator[CsvSinkFormat, None, None]:
        blob = self._bucket.get_blob(file_name, client=self._storage_client)
        blob_io = StringIO(blob.download_as_string().decode('utf-8'))
        reader = csv.reader(blob_io)
        group = next(reader)[1]
        date_format = next(reader)[1]
        header = next(reader)
        for row in reader:
            try:
                yield CsvSourceFormat.from_dict_to_sink(
                    dict(zip(header, row)),
                    file_name=file_name,
                    group=group,
                    date_format=date_format
                )
            except ValueError:
                continue
