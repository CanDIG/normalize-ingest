#!/usr/bin/env bash

set -xe

source "$(pwd)"/.env
shopt -s expand_aliases
alias mc="docker exec -it $(basename "`pwd`")_mc_1 mc"

mc config host add minio http://minio:9000 $MINIO_ACCESS_KEY $MINIO_SECRET_KEY --api S3v4

#mc admin config export --json minio \> /tmp/minio-config-original.json

#mc mb minio/config
mc mb minio/samples/processed/
mc mb minio/samples/unprocessed/

mc admin config set minio notify_webhook:1 queue_limit="0" endpoint="http://listener:8080/events"
mc admin service restart minio

mc event add minio/samples/unprocessed/ arn:minio:sqs::1:webhook --event put --suffix .vcf.gz

mc event list minio/samples

#mc admin config export --json minio \> /tmp/minio-config-webhook.json
#mc cp /tmp/minio-config-*.json minio/config/

mc watch minio/samples/unprocessed
