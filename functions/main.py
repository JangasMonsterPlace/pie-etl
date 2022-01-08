import json
import google.cloud.functions.context

from flask import Request
import functions_framework

from google.oauth2 import service_account
from google.cloud import workflows_v1beta
from google.cloud.workflows import executions_v1beta

from common.settings import GCP_Project, ETL_Workflow


@functions_framework.http
def load_to_bigquery(request: Request) -> str:
    return "Hello BigQuery"


@functions_framework.http
def load_to_elasticsearch(request: Request) -> str:
    return "Hello Elasticsearch"


def trigger_etl_pipeline(event: dict, context: google.cloud.functions.context):
    arguments = {"file_name": event["name"]}

    credentials = service_account.Credentials.from_service_account_file(GCP_Project.CREDENTIALS_FILE_PATH.value)
    execution_client = executions_v1beta.ExecutionsClient(credentials=credentials)
    execution = executions_v1beta.Execution(argument=json.dumps(arguments))
    workflows_client = workflows_v1beta.WorkflowsClient(credentials=credentials)

    parent = workflows_client.workflow_path(
        project=GCP_Project.PROJECT.value,
        location=ETL_Workflow.LOCATION.value,
        workflow=ETL_Workflow.NAME.value
    )
    execution_client.create_execution(parent=parent, execution=execution)
