#! /bin/sh

RED='\033[0;31m'
NC='\033[0m'

docker ps

echo -e "${RED}killing containers, enter the containerID${NC}"
read cont1
read cont2
docker kill $cont1 $cont2
docker rm $cont1 $cont2

echo -e "${RED}removing rest${NC}"
docker system prune -a
docker volume rm blockstore
docker network prune

echo -e "${RED}check the processes${NC}"
docker container ls
echo -e "${RED}Images${NC}"
docker image ls
echo -e "${RED}Volumes${NC}"
docker volume ls
echo -e "${RED}Network${NC}"
docker network ls
