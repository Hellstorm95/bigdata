from pymongo import MongoClient
from pymongo import errors as mongoerrors
from pymongo import WriteConcern
import json
import datetime
import time

f = open("worldwide_covid.json", "r") 
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
	#collection = db["EUData"]
	collection = db["EUData"].with_options(write_concern=WriteConcern(w="majority"))
	start = time.time()
	for chunk in chunks:
		collection.insert_many(chunk)
		#collection.insert_many(chunk)
	end = time.time()
	f = open("response_time.txt", "w")
	f.write(str(end - start))
	f = open("errors.txt", "w")
	f.write("None")
except mongoerrors.PyMongoError as e:
	f = open("response_time.txt", "w")
	f.write("error")
	f = open("errors.txt", "w")
	f.write(str(e))

