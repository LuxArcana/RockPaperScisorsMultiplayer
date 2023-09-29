to build docker image
cd src
docker build -t rockpaperscisorsweb:v1 ./

to start docker image server
cd src
docker compose up
    add -d to run as daemon

to stop docker image server
docker compose down





TODO: player move timeout.
    allow contest creator to set the maximum time to wait for a player move
    when this time is exceeded, the host service will set the move to none for any players that have not yet made a move

TODO:
    refactor RockPaperScisorsConsoleUI.PlayContest
    this method is to long