#!/bin/bash

SERVICE_NAME="notion-service-hub"

CUSTOM_PORT="8000"

ENV_VARS=""
while IFS='=' read -r key value; do
  # Skip empty lines or comments
  if [[ -n "$key" && "$key" != \#* ]]; then
    if [[ -n "$ENV_VARS" ]]; then
      ENV_VARS="$ENV_VARS,$key=$value"
    else
      ENV_VARS="$key=$value"
    fi
  fi
done < .env

gcloud run deploy "$SERVICE_NAME" \
  --set-env-vars "$ENV_VARS" \
  --port="$CUSTOM_PORT"
