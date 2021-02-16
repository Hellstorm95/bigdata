# Assignment-1-Report

## Part 1 - Design 

### 1)
I choose to focus on the COVID datasets because it is now topical and seemed the most interesting. I for this assignemnt I chosen to use the [EU dataset]().

I have chosen to use MongoD for my platform. The main reason I choose MongoDB for the mysimbdp-coredms component is the flexibility in schema it provides. This is important for the COVID datasets because there are various types of datasets which stores different types of data. For instance there are datasets which shows the daily and weekly new cases and deaths and there are datasets which show hospital admission rates, both of which have different schemas.  Other reasons for using MongoDB is that it seem quite popular and therefore there exists support when I run into trouble, and lastly there is python package for MongoDB which is my programming language of choice.

I decided docker containers as test deployment enviroment as it abled me to test and prove my design locally without using monetary resources on cloud services.

### 2)
In my design at this moment, the mysimbdp-daas is directly connected to mysimbdp-coredms. The external data producers/consumers call the mysimbdp-daas and mysimbdp-daas calls the API of mysimbdp-coredms. mysimbdp-dataingest takes data from a file from a customer by some script (or comamand) created by the customer. The customer's script uses the python code mysimbdp-dataingest which reads the file and the contents of the file is then ingested into mysimbdp-coredms by calling its API. Both mysimbdp-daas and mysimbdp-dataingest are connected to mysimbdp-coredms but they are not connected to each other.

### 3)
In MongoDB a cluster of nodes, (called a replica set), have three nodes. One node is primary and handles all writes, the other two are secondary nodes can handle reads but does not handle writes. When the primary node fails, one of the two secondary nodes elect themselves as a primary node. All of the nodes hold the same data. This way there are always a primary node that can read and write data. There is another MongoDB way to to create a replica set using an arbiter node instead of a third secondary node but I will not use that kind of replica set.

### 4)
In a MongoDB replica set, the primary node saves an operation log which saves all of changes done to the database. The secondary nodes copies the operation log asynchronously and performs the changes themselves according to the operation log. In MongoDB sharding is done by creating a proxy that works as a router that divides the data into different chunks and spreads out the chunks into different shard replica sets. The router forwards a data document to the correct replica set by checking a sharding key of the document and checking with a config server that is a replica set which holds metadata and configuration of the clusters. The sharding key is field of the documents chosen for a collection and can be hashed and then divided into a range of values or directly be divided according to the range of values. So at minimum the mysimbdp-coredms needs 3 nodes for config replica set, 1 node for the router, if the router node is down, more nodes have to be added, and 6 nodes for two shard data replica sets. 

### 5)
I would scale mysimbdp horizontally by creating more shard replica sets for mysimbdp-coredms and more routers. Veritcally I would scale by deploying the service to the cloud adn buying more computation power. 

## Part 2 - Implementation 

### 1)
In MongoDB there exists databases and collections. In my datastructure there exists only one MongoDB database on mysimbdp-coredms but the customers can create different collections. MongoDB has a document-oriented model and essentially any JSON document can be uploaded. For this assignment I assume each customer will want a collection of their own for each dataset and not have two different types of datasets in one collection. Each document in a collection is an entry in a dataset. 

### 2)
The sharding procedure is explained in Part 1, Point 4, but the I will now explain which sharding key I and sharding method, (hashed vs non-hashed sharding,) I used for this assignment. For the EU data I have chosen the sharding key "country" and to use non-hashed sharding as there are many countries, create a suitable range and is field that exists in most COVID datasets. I think hashed sharding would be more useful when there are a lot of options for the value of the field and for fields such as the date of data taken as the range would grow larger every day it is taken.

### 3)

### 4)

### 5)


## Part 3 - Extension 

### 1)
I would create a collection that stores the metadata for each collection and each time data is changed it is updated by mysimbdp-daas and mysimbdp-dataingest depending on which is used.

### 2)
If I would publish to consul I would use this format:
{
  "name":"'user_mongodb'",
  "tags":["covid"],
  "port": 27017,
  "address":"0.0.0.0",
}
'user_mongodb' should be replaced with a customer's username and the adress "0.0.0.0" should be replaced with the adress to the costumer's mysimbdp-coredms.

### 3)
mysimbdp-dataingest needs now to get the address of the correct user. mysimbdp-dataingest now takes the service list from consul service discovery and then gets the correct address and then calls the API of mysimbdp-coredms with the adress.

### 4)
mysimbdp-dataingest
