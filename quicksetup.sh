#! /bin/sh

RED='\033[0;31m'
NC='\033[0m'

echo -e "${RED}Pulling latest docker image${NC}"
docker pull hyperledger/iroha:latest

echo -e "${RED}Creating Docker network${NC}"
docker network create iroha-network

echo -e "${RED}setting up POSTGRESQL${NC}"
docker run --name some-postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 --network=iroha-network -d postgres:9.5 -c 'max_prepared_transactions=100'

echo -e "${RED}Creating Volume${NC}"
docker volume create blockstore

echo -e "${RED}Running IROHAD${NC}"
docker run --name iroha -d -p 50051:50051 -v $(pwd)/myconfig:/opt/iroha_data -v blockstore:/tmp/block_store --network=iroha-network -e KEY='node0' hyperledger/iroha:latest

echo -e "${RED}Testing${NC}"
docker ps
sudo netstat -tulpn | grep LISTEN
