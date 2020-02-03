#!/usr/bin/env bash

set -xe

docker-compose rm -v -f
docker volume prune -f
docker network prune -f
