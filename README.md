# Functions with Google CLI

Upload etl process with Google cli
```
~/google-cloud-sdk/bin/gcloud functions deploy {{ SERVICE_NAME }} \
  --source etl/ \
  --runtime python38 \
  --allow-unauthenticated \ 
  --trigger-http 
```

Test HTTP Triggered function
```
curl -X GET https://us-central1-easy-as-pie-hackathon.cloudfunctions.net/{{ FUNCTION_NAME }}
```


Upload File Triggered Function
```shell
~/google-cloud-sdk/bin/gcloud functions deploy trigger_etl_pipeline \
--source etl/ \
--runtime python38 \
--trigger-event google.storage.object.finalize \
--trigger-resource bic-review-data
```

# Workflows with Google CLI

```
~/google-cloud-sdk/bin/gcloud workflows deploy etl \
--source etl.workflow.yaml
```

Execute Workflow via API
- get started with authentication https://cloud.google.com/docs/authentication/getting-started#command-line
- 


```shell
curl \
  --request POST \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer "$(~/google-cloud-sdk/bin/gcloud auth application-default print-access-token)' \
  "https://workflowexecutions.googleapis.com/v1/projects/easy-as-pie-hackathon/locations/us-central1/workflows/etl/executions"
```