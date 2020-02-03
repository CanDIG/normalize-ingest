#!/usr/bin/env bash

set -xe

docker-compose build
#docker rmi $(docker images | grep "<none>" | awk '{print $3}')
docker-compose up
