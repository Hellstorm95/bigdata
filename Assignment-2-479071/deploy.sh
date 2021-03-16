#!/bin/bash
sudo docker build --tag ingestion  ./ingestion_image
sudo docker build --tag rq_worker ./redis
sudo docker build --tag api ./IngestionApp
sudo docker-compose up --remove-orphans -d
sleep 20
sudo docker-compose exec config01 sh -c "mongo --port 27017 < /scripts/init-configserver.js"
sudo docker-compose exec shard01a sh -c "mongo --port 27018 < /scripts/init-shard01.js"
sudo docker-compose exec shard02a sh -c "mongo --port 27019 < /scripts/init-shard02.js"
sudo docker-compose exec shard03a sh -c "mongo --port 27020 < /scripts/init-shard03.js"
sleep 60
sudo docker-compose exec router sh -c "mongo < /scripts/init-router.js"
sleep 5
sudo docker exec assignment-2-479071_client_1 python3 load_script.py
sleep 60


sudo docker-compose down
sudo docker rm -f $(docker ps -a -q)
sudo docker volume rm $(docker volume ls -q)


