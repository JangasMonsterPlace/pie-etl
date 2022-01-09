import json
import google.cloud.functions.context

from flask import Request
import functions_framework

from google.oauth2 import service_account
from google.cloud import workflows_v1beta
from google.cloud.workflows import executions_v1beta
from google.cloud import bigquery

from common.settings import GCP_Project, ETL_Workflow
from common import extract_csv


@functions_framework.http
def load_to_bigquery(request: Request) -> str:
    client = bigquery.Client(credentials=GCP_Project.CREDENTIALS.value)
    with extract_csv.CloudStorageLoader() as source:
        client.insert_rows_json(
            "easy-as-pie-hackathon.nlp.raw-data",
            json_rows=[row.__dict__ for row in source.load_csv_data("DisneylandReviews.csv")]
        )
    return "Hello BigQuery"


@functions_framework.http
def load_to_elasticsearch(request: Request) -> str:
    with extract_csv.CloudStorageLoader() as source:
        for row in source.load_csv_data("DisneylandReviews.csv"):
            continue
    return "Hello Elasticsearch"


def trigger_etl_pipeline(event: dict, context: google.cloud.functions.context):
    arguments = {"file_name": event["name"]}

    execution_client = executions_v1beta.ExecutionsClient(credentials=GCP_Project.CREDENTIALS.value)
    execution = executions_v1beta.Execution(argument=json.dumps(arguments))
    workflows_client = workflows_v1beta.WorkflowsClient(credentials=GCP_Project.CREDENTIALS.value)

    parent = workflows_client.workflow_path(
        project=GCP_Project.PROJECT.value,
        location=ETL_Workflow.LOCATION.value,
        workflow=ETL_Workflow.NAME.value
    )
    execution_client.create_execution(parent=parent, execution=execution)


if __name__ == "__main__":
    load_to_bigquery(None)
