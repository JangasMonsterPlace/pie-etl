import csv
from io import StringIO
from dataclasses import dataclass
from datetime import date
from dataclasses_jsonschema import JsonSchemaMixin
from typing import Generator, List

from google.cloud import storage
from google.cloud import bigquery

from .settings import GCP_Project, GCP_Storage


BIG_QUERY_TYPE_MAPPER = {
    "<class 'str'>": "STRING",
    "<class 'int'>": "INTEGER",
    "<class 'datetime.date'>": "DATE",
}


@dataclass
class CsvSinkFormat(JsonSchemaMixin):
    source_type: str
    source: str
    review_id: str
    rating: int
    date: str
    text: str

    def get_big_query_parameters(self) -> List[bigquery.ScalarQueryParameter]:
        parameters = []
        for field_name, d_type in self.__annotations__.items():
            parameters.append(
                bigquery.ScalarQueryParameter(
                    name=field_name,
                    type_=BIG_QUERY_TYPE_MAPPER[str(d_type)],
                    value=self.__dict__[field_name]
                )
            )
        return parameters


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
        self._storage_client = storage.Client(credentials=GCP_Project.CREDENTIALS.value)
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
