# Assignment-3-Report

## Part 1 - Design for streaming analytics

### 1)
I have chosen the [BTS dataset](https://version.aalto.fi/gitlab/bigdataplatforms/cs-e4640/-/blob/master/data/bts/README.md). 
Each station has an id, each station has sensors which measures different data and each sensor data has an id.
If the value of a sensor goes over a threshold an alarm can be sent. Each alarm type has an id. 
Each data row is representing an alarm which has been sent from a station, has included the station id, alarm id and the sensor id.

(i) A streaming analytic the tenant wants to perform is to calculate the frequency of alarms of all types for a sensor from each of the stations and 
mark down the sensor having a problem if the frequency is higher than a threshold. 

(ii) A batch analytic would be checking the amount of marked problems of a sensor.

### 2)
(i) The data streams should be partitioned by the key "station id", enabling parallell processing, and partitioning the records
already according to the different station. The amount of data coming from each station should be about the same so
the workload for each node processing the data should be about the same.

(ii) For event delivery it is important that the delivery guarantee is Exactly Once, since we want accurate info regarding
the frequency if of the alarms and if there are missing or too many alarm events sent the analytics is going to be wrong.
For the result delivery it is not that important if there are multiple results outputted to the sink but we want the 
results At Least Once.

### 3)
(i) For the dataset chosen, for each data item there is an event time stored and is the most suitable time to use 
as we want to calculate the amount of alarms triggered in a set of time and the event time stored in the data is the most accurate.
If there were no event time stored in the data, I think the best solution would be to take the time in which the event arrived 
to the streaming data processing service.
 
(ii) The tumbling window identified by time. We can use the amount of a certain type of alarm events
from a certain sensor inside the time of window and the fixed window size to calculate the frequency of alarms. 
For instance, there are 40 alarms of type A from sensor A in a window of 10s. 

(iii)
If the alarm event would arrive later than the window of time, then the event would not be calculated in the frequency
when the processing function has already calculated it and marked a problem for a sensor. 

(iv)
Yes, I would use a watermark as it enables alarm events to come later than the window and still be calculated in the 
frequency by the processing function. For aspect (iii), the event could still be too late if it is later than the 
watermark.

### 4)
For my tenant scenario, the metric that would be streaming analytics alarm/s. It is measured by calculating the amount of alarms
divided by the window size. It is important for the tenant because high amount of alarms of a sensor indicates a problem
with sensor or something wrong with station.
 