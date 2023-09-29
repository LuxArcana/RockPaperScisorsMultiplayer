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
    Factor Out Magic Strings
    mostly gameState and contestState values

TODO:
    refactor RockPaperScisorsConsoleUI.PlayContest
    this method is to long

TODO:
    fix location of build game response DTO

TODO:
    Add DB Backend to increase thread count

TODO:
    add api service configuration object

TODO:
    add client service configuration object

TODO:
    add acme certificate managment and https to NGINX reverse proxy

TODO(MABEY):
    add html version of client