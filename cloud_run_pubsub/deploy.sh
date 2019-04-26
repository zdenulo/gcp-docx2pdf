#!/usr/bin/env bash

gcloud builds submit --config=cloudbuild.yaml --substitutions=_SERVICE_NAME="sa-run",TAG_NAME="v0.0.2",_ENV_VARIABLES="OUTPUT_BUCKET=gcs-upload-test"