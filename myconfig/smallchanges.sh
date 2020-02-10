#! /bin/sh

RED='\033[0;31m'
NC='\033[0m'

echo -e "${RED}deleting IROHAD enter containerID${NC}"
read cont
docker kill $cont
docker rm $cont

echo -e "${RED}Reloading IROHAD${NC}"
docker run --name iroha -p 50051:50051 -d -v $(pwd)/myconfig:/opt/iroha_data -v blockstore:/tmp/block_store -e POSTGRES_HOST='some-postgres' -e POSTGRES_PORT='5432' -e POSTGRES_PASSWORD='mysecretpassword' -e POSTGRES_USER='postgres' -e KEY='node0' \
--network=iroha-network \
hyperledger/iroha:latest

echo -e "${RED}test${NC}"
docker ps
