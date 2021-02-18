#!/bin/bash
sudo docker build --tag ingestion  ../ingestion_image
sudo docker-compose up --remove-orphans -d
sleep 20
sudo docker-compose exec config01 sh -c "mongo --port 27017 < /scripts/init-configserver.js"
sudo docker-compose exec shard01a sh -c "mongo --port 27018 < /scripts/init-shard01.js"
sudo docker-compose exec shard02a sh -c "mongo --port 27019 < /scripts/init-shard02.js"
sudo docker-compose exec shard03a sh -c "mongo --port 27020 < /scripts/init-shard03.js"
sleep 60
sudo docker-compose exec router sh -c "mongo < /scripts/init-router.js"
sleep 5
for i in $(seq 1 10)
do
	sudo docker exec -d 10_customers_client_$i python3 mysimbdp-dataingest.py
done
sleep 120
for i in $(seq 1 10)
do
	sudo docker cp 10_customers_client_$i:response_time.txt response_time_$i.txt
	sudo docker cp 10_customers_client_$i:errors.txt errors_$i.txt
done

for i in $(seq 1 10)
do
	sudo cat response_time_$i.txt >> response_times.txt  
	sudo printf "\n" >> response_times.txt  
	sudo rm response_time_$i.txt
	sudo cat errors_$i.txt >> errors.txt
	sudo printf "\n" >> errors.txt  
	sudo rm errors_$i.txt
done

sudo docker-compose down
sudo docker rm -f $(docker ps -a -q)
sudo docker volume rm $(docker volume ls -q)



