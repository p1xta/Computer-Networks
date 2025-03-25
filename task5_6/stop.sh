#!/bin/bash

docker stop api_container db_container
docker rm api_container db_container
docker rmi task5_app

docker network rm task5_network

echo "Containers stopped"