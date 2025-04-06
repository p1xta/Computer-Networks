#!/bin/bash

docker stop nginx_container api_container db_container
docker rm nginx_container api_container db_container
docker rmi task5_app

docker network rm task5_network

echo "Containers stopped"