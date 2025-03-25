#!/bin/bash

docker network create task5_network

docker build -t custom_postgres -f Dockerfile.postgres .

docker run -d \
  --name db_container \
  --network task5_network \
  --env-file .env \
  -p 5432:5432 \
  custom_postgres

docker build -t task5_app .
docker run -d \
  --name api_container \
  --network task5_network \
  --env-file .env \
  -p 1111:8080 \
  task5_app

echo "Containers started"