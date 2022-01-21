gcloud functions \
  deploy ${FUNCTION_NAME_HTTP} \
  --source=${SOURCE_DIR} \
  --runtime=python37 \
  --trigger-http \
  --allow-unauthenticated