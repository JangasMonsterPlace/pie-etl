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


# Workflows with Google CLI

```
~/google-cloud-sdk/bin/gcloud workflows deploy etl \
--source etl.workflow.yaml
```