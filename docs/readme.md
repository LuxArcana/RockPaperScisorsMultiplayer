to build docker image
cd src
docker build -t rockpaperscisorsweb:v1 ./

to start docker image server
cd src
docker compose up
    add -d to run as daemon

to stop docker image server
docker compose down
