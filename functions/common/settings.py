import os
from enum import Enum


BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class GCP_Project(Enum):
    CREDENTIALS_FILE_PATH = os.path.join(BASE_DIR, ".google-service-account-file.json")
    PROJECT = "easy-as-pie-hackathon"


class ETL_Workflow(Enum):
    LOCATION = "us-central1"
    NAME = "etl"
