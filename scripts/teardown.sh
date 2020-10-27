#!/usr/bin/env bash

docker kill $(docker ps -q)
docker rm $(docker container ls -aq)
