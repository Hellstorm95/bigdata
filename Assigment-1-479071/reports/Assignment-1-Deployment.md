# Assignment-1-Deployment

For the depoyment to work you will need docker and docker-compose. To recreate the tests you will have to go to the directory /code and choose one of the "x_customers" directories depending on which you want to test. Once you are in the correct directory just use the command "sh deploy.sh". Be AWARE!!! deploy.sh deletes all of the containers and columes after running!!!. If you want to not delete those comment out the last two lines in the deploy.sh.

I have used the latest version of MongoDB docker image. I also have used python3 for the python programs.

If you want turn on or off the consistency option comment out one of the "collection = db["EUData"]" and uncomment the other one in the python code "mysimbdp-dataingest.py" located into the "ingestion_image". The one with the ".with_options(write_concern=WriteConcern(w="majority"))" is the one with consistency option enabled.

If you want to create the charts run the the python code create_charts.py. For create_charts.py you will need to run "pip3 install matplotlib".  
