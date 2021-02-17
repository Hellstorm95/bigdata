from pymongo import MongoClient
from pymongo import errors as mongoerrors
import json
import datetime
import time

f = open("worldwide_covid.json", "r") 
parsed_json = json.loads(f.read())
f.close() 

try:
	client = MongoClient("router", 27017)
	db = client["covid"]
	collection = db["EUData"]
	start = time.time()
	collection.insert_many(parsed_json["records"])
	end = time.time()
	f = open("response_time.txt", "w")
	f.write(str(end - start))
	f = open("errors.txt", "w")
	f.write("None")
except mongoerrors.PyMongoError as e:
	f = open("response_time.txt", "w")
	f.write(str(end - start))
	f = open("errors.txt", "w")
	f.write(e)
