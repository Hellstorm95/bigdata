import pika
import sys
from pymongo import MongoClient
from pymongo import errors as mongoerrors
import json
import requests
import time

messages = 0
start_time = time.time()
ingestion_times = 0
ingestions = 0
total_size = 0

def callback(ch, method, properties, body):
    user = 'user2'
    global messages
    global start_time
    global ingestion_times
    global ingestions
    global total_size
    
    messages += 1
    end_time = time.time()
    if end_time - start_time > 5:
        if ingestions == 0:
            avg_ingesttime = 0
        else:
            avg_ingesttime = ingestion_times / ingestions
        url = 'http://flask_service:80/log'
        response = requests.post(url, data={'user': user, 'avg_ingesttime': avg_ingesttime, "tot_size": total_size, "messages": messages})
        print(response)
        messages = 0
        start_time = time.time()
        ingestion_times = 0
        ingestions = 0
        total_size = 0
    
    try:
        client = MongoClient("router", 27017)
        db = client["covid"]
        collection = db["EUData"]
        start = time.time()
        collection.insert(json.loads(body))
        end = time.time()
        
        total_size += sys.getsizeof(body)
        ingestion_times += end - start
        ingestions += 1
        
    except mongoerrors.PyMongoError as e:
        url = 'http://flask_service:80/log_error'
        response = requests.post(url, data={'user': user, 'error': e})
        print(response)
