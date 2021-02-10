#Assignment-1-Report

1)
I chose to focus on the domain Mobility/Transportation because I want to see how difficult it is to keep and maintain a huge database of structured data. For this assignment I specifically chose the [Chicago Taxi Dataset](https://data.cityofchicago.org/Transportation/Taxi-Trips/wrvz-psew) because it has many types of data types and even empty cells in the csv.

I chose to use MariaDB for mysimbdp-coredms because the relational database model has powerful querying and consistency support. The querying is really important because we want to be able filter out a lot of data to find the data we actually want, for instance, we may want to find out which taxis were active a certain day or we want find what trips a certain taxi did a certain day. The consistency support is also important as the data provided needs to stay conistant for each taxi trip. Relational models have strict schema requirements but it is not a problem when it comes to the data needed and provided from taxi trips, calls, sms and internet accesses is not going to change, at least not often.

I have chosen to deploy the platform with docker swarm as it provided an easy local way to test my design. I have chosen Galera clustering for the clustering as it works with MariaDB and provides less latency, read scalability and no lost transactions. 
