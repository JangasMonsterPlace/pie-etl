from flask import Request
import functions_framework


@functions_framework.http
def load_to_bigquery(request: Request) -> str:
    return "Hello BigQuery"


@functions_framework.http
def load_to_elasticsearch(request: Request) -> str:
    return "Hello Elasticsearch"
