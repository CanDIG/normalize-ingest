#!/usr/bin/env bash

set -xe

mkdir -p bin

curl -Lo $(pwd)/bin/minio \
		https://dl.minio.io/server/minio/release/linux-amd64/minio
curl -Lo $(pwd)/bin/mc \
		https://dl.minio.io/client/mc/release/linux-amd64/mc

chmod 755 $(pwd)/bin/minio
chmod 755 $(pwd)/bin/mc

