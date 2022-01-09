import os
from enum import Enum

from google.oauth2 import service_account


BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class GCP_Project(Enum):
    CREDENTIALS = service_account.Credentials.from_service_account_file(
        os.path.join(BASE_DIR, ".google-service-account-file.json")
    )
    PROJECT = "easy-as-pie-hackathon"


class ETL_Workflow(Enum):
    LOCATION = "us-central1"
    NAME = "etl"


class GCP_Storage(Enum):
    BUCKET_NAME = "bic-review-data"
