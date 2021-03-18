# Assignment-2-Deployment

To run test for batch ingestion you go to the directory code/batch_assignment and run "sh deploy.sh". The logs from the run are saved in the "data" directory.
To open the redis dashboard to see some stats on the redis queue use the url http://localhost:9181 in your browser. To calculate the average runtime of batchingestapp run the script "calc_avg_runtime".py. 

To run test for stream ingestion you go to the directory code/stream_assignment and run "sh deploy.sh". The logs from the run are saved in the "data" directory.
To open the RabbitMQ dashboard to see some stats on the RabbitMQ queue use the url http://localhost:15672 in your browser. Login with guest as userename and guest as password.
 
Be AWARE!!! deploy.sh deletes all of the containers and columes after running!!!. If you want to not delete those comment out the last two lines in the deploy.sh.

I have used the latest version of MongoDB, Redis, and RabbitMQ docker image . I also have used python3 for the python programs.
