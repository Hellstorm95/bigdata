#!/bin/bash
sudo docker build --tag stream_ingestion1 ./stream_client1
sudo docker build --tag stream_ingestion2 ./stream_client2
sudo docker build --tag stream_api ./IngestionApp
sudo docker-compose up --remove-orphans -d
sleep 20
sudo docker-compose exec config01 sh -c "mongo --port 27017 < /scripts/init-configserver.js"
sudo docker-compose exec shard01a sh -c "mongo --port 27018 < /scripts/init-shard01.js"
sudo docker-compose exec shard02a sh -c "mongo --port 27019 < /scripts/init-shard02.js"
sudo docker-compose exec shard03a sh -c "mongo --port 27020 < /scripts/init-shard03.js"
sleep 60
sudo docker-compose exec router sh -c "mongo < /scripts/init-router.js"
sleep 5
sudo docker exec -d stream_assignment_client1_1 python3 senddata.py
sudo docker exec -d stream_assignment_client2_1 python3 senddata.py
sleep 1010

sudo docker-compose down
sudo docker rm -f $(docker ps -a -q)
sudo docker volume rm $(docker volume ls -q)


