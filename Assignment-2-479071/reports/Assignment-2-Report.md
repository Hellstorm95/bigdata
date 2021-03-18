For mysimbdp-coredms I use the same Mongo server setup I used in the first assignment.

# Part 1

## 1)
I think the most important things is to constrain the batch ingestion tenants is the amount of files and the file size because we do not want the tenants to overload the whole platform. The tenants will upload their files for staging through an API called batch-api.

Here is the example config file for the API.

class Config(object):
    MAX_NUMBER_OF_FILES = 10
    MAX_FILE_SIZE = 4000000000

class NormalConfig(Config):
    pass
    
Here the user is allowed to ingest 10 files with a maximum size of 4GB in one ingestion. 

##2)
Clientbatchingest takes a csv filename as input and loads the file. The file is converted into python dict which the same form as a json document and then the whole document is ingested into mongo server sink with pymongo command insertMany(). If the ingestion creates any errors the error is returned otherwise it just return None.

##3)
The clientbatchapp must only take a filename as input and return None if no error was raised or return the error. In order for the tenant to ingest, the user must first call the API batch-api to load the script file into mysimbdp. The script file is saved into a directory which is specific for a user. The tenant then calls again batch-api in order to load the data files. The files are then stored in the same directory as the script. The directory is a shared volume between the containers. After the files are stored in the directory, the ingestion of the files are then queued into a Redis queue. In my enviroment I have a Redis server, a queue and three workers which perform the ingestions. The queue is is first in and first out. Once one ingestion is done, a worker takes one of the ingestion task from the queue. 

##4)
Every tenant has an own directory for their ingestion script and the staged files. The Redis queues and workers are shared with between all the tenants. For the tests I have used two separate clients with the same scripts and same data files. Both clients ingest 5 of a 4.3MB file, making it 10 files to be ingested in total. For this test the tenants don't have to register a user, they just put the user in the with API calls. 

##5)
In order to log the ingestions the client ingestion script is nested in another logging script that takes the output from the client script and takes the time for the ingestion script and logs it into the correct directory. The logging script also saves to general log which stores ingestion stats from all of the users. The logging script is the actual script which is input to the redis queue. 

# Part 2

For the stream ingestion I have used RabbitMQ as it supports python and had good documentation. 

## 1)
Each user has their directory for clientstreamingestapp, logs and the tags for each consumer for the messaging queue. Each user has their own consumers for their messages and their own queue. Each user has one queue which they can use. The users are constrained on the size of input and the amount of messages, in a set amount of time (e.g. 5 seconds). The stream-api enforces them when the API gets log messages from clientstreamingestapp, the logging system is explained later, and the constraints are saved in the API config file like in batch ingestion.

Here is how the config file looks like:

class Config(object):
    MAX_NUMBER_OF_MESSAGES = 500
    MAX_SIZE = 4000000000

class NormalConfig(Config):
    pass
    
In this config file the maximum amount of messages is 500 and the maximum data size in 5 seconds is 400MB. 

##2)
For a user to use the platform, the user needs to call the API stream-api to start a queue and a consumer. The user posts clientstreamingestapp and the api creates a queue and a consumer for the clientstreamingestapp. The user then send messages to the queue to ingest the data and call the API to stop the consumer and the queue. clientstreamingestapp has to work as a callback function for a rabbitMQ, meaning it has to take four arguments ch, method, properties, body and it does not return anything.

## 3)
clientstreamingestapp just takes the body of the message which is a json document and ingest it immediately into the mongo server. For the test I have two users with the same clientstreamingestapp. They both ingest a 4.3MB json file one item at a time, meaning there is a for loop going through the file sending an item to the RabbitMQ queue. 

## 4)
clientstreamingestapp saves the amount of messages, the average ingestion times and the total data size within a 5 seconds time interval. clientstreamingestapp calls the stream-api every five seconds in order to log the stats. If the clientstreamingestapp gets an error, the error is sent to be logged with the stream-api.

## 5)
Every time the stats are logged, the stream-api checks the stats and either adds or removes consumers according to the amount of messages that have been handled. In my test enviroment the stream-api checks for the amount of messages within a 5 second limit and adds or removes consumers accordingly. It also checks if the amount of messages and the size of data exceeds the constraints. If it exceeds the constraints the queue and the consumer is deleted. It is able to delete consumers with the consumer tags which are saved for each user.


# Part 3

## 1)
I could use an API for logging for both the batch and stream ingest to make the logs. The logging script in the batch ingestion would now call the API for logging and the stream ingestion app already calls an API for logging. If I don't want to rely on the tenant to call the API in stream ingestion, I could use a nested function like in batch ingestion as a callback function for the consumers and instead return the data from clientstreamingestapp and make the top nested logging function call the API and log the data.

## 2)
I would make it possible to create multiple queues for each user instead of having only one queue dedicated to the tenant. Each queue would be coupled with a different clientstreamingestapp created by the tenant and each clientstreamingestapp would ingest into different sinks. The tenant would just use the right queue for the right sink. 

## 3)
RabbitMQ is able to handle TLS connections https://www.rabbitmq.com/ssl.html. I would configure the RabbitMQ server to handle TLS connection. The user would then able to create clientstreamingestapp and connect to the queue with the correct security keys.

## 4)
I would expand the API so that the tenant can upload a data quality checker and a metadata producer and ingestor which are used when the tenant uploads the ingestion data to the API. 

## 5)
For batch ingestion would make it possible for the tenant to upload more clientbatchingestapp and when the tenant uploads files to be ingested I would also make it mandatory for the tenant to specify which clientbatchingestapp should be used for the data.

For stream ingestion I would make it possible to create multiple queues for each user instead of having only one queue dedicated to the tenant. Each queue would be coupled with a different clientstreamingestapp created by the tenant. The tenant then chooses which queue they want to use according to their preferences. 

