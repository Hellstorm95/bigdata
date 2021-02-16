# Assignment-1-Report

## 1)
I choose to focus on the COVID datasets because it is now topical and seemed the most interesting. The main reason I choose MongoDB for the mysimbdp-coredms component is the flexibility in schema it provides. This is important for the COVID datasets because there are various types of datasets which stores different types of data. For instance there are datasets which shows the daily and weekly new cases and deaths and there are datasets which show hospital admission rates, both of which have different schemas.  Other reasons for using MongoDB is that it seem quite popular and therefore there exists support when I run into trouble, and lastly there is python package for MongoDB which is my programming language of choice.

I decided docker containers as test deployment enviroment as it abled me to test and prove my design locally without using monetary resources on cloud services.

## 2)
In my design at this moment, the mysimbdp-daas is directly connected to mysimbdp-coredms. The external data producers/consumers call the mysimbdp-daas and mysimbdp-daas calls the API of mysimbdp-coredms. mysimbdp-dataingest takes data from a file from a customer by some script (or comamand) created by the customer. The customer's script uses the python code mysimbdp-dataingest which reads the file and the contents of the file is then ingested into mysimbdp-coredms by calling its API. Both mysimbdp-daas and mysimbdp-dataingest are connected to mysimbdp-coredms but they are not connected to each other.

## 3)
In MongoDB a cluster of nodes, (called a replica set), have three nodes. One node is primary and handles all writes, the other two are secondary nodes can handle reads but does not handle writes. When the primary node fails, one of the two secondary nodes elect themselves as a primary node. All of the nodes hold the same data. This way there are always a primary node that can read and write data. There is another MongoDB way to to create a replica set using an arbiter node instead of a third secondary node but I will not use that kind of replica set.

## 4)
In a MongoDB replica set, the primary node saves an operation log which saves all of changes done to the database. The secondary nodes copies the operation log asynchronously and performs the changes themselves according to the operation log. In MongoDB sharding is done by creating a proxy that works as a router that divides the data into different chunks and spreads out the chunks into different shard replica sets. The router forwards a data document to the correct replica set by checking a preset sharding key of the document and checking with a config server that is a replica set which holds metadata and configuration of the clusters. The sharding key can be hashed and then divided into a range of values or directly be divided according to the range of values. So at minimum the mysimbdp-coredms needs 3 nodes for config replica set, 1 node for the router, if the router node is down, more nodes have to be added, and 6 nodes for two shard data replica sets. 

## 5)
I would scale mysimbdp horizontally by creating more shard replica sets for mysimbdp-coredms and more routers. Veritcally I would scale by deploying the service to the cloud adn buying more computation power. 
