import pika
import sys

def callback(ch, method, properties, body):
    data = json.loads(body)
    user = 'test1'"
    try:
	client = MongoClient("router", 27017)
	db = client["covid"]
	collection = db["EUData"]
	start = time.time()
	for chunk in chunks:
		collection.insert(chunk)
	end = time.time()
	size = sys.getsizeof(body)
	runtime = (str(end - start))
	url = 'http://0.0.0.0:56733/log'
	response = requests.post(url, data={'user': user, 'runtime': runtime, "size": size})
except mongoerrors.PyMongoError as e:
        url = 'http://0.0.0.0:56733/log_error'
        response = requests.post(url, data={'user': user, 'error': e})
	
    
