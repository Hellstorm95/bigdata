from pymongo import MongoClient
from pymongo import errors as mongoerrors
from pymongo import WriteConcern
import json
import datetime
import time

def ingest_file(filename):
    f = open(filename, "r") 
    parsed_json = json.loads(f.read())
    f.close() 

    chunk_size = 100
    num_chunks = int(len(parsed_json["records"]) / chunk_size)
    chunks = []
    for i in range(num_chunks):
        chunks.append(parsed_json["records"][chunk_size*i:chunk_size*(i+1)])
        
    chunks.append(parsed_json["records"][chunk_size*num_chunks:])
    try:
        client = MongoClient("router", 27017)
        db = client["covid"]
        collection = db["EUData"]
        for chunk in chunks:
            collection.insert_many(chunk)
    
    except mongoerrors.PyMongoError as e:
        return error
