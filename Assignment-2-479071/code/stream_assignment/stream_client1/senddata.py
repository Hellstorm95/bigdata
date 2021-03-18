import pika
import json
import time
import requests

url = 'http://flask_service:80/start'
user = {'user': 'user1'}
f = {"file": open("clientstreamingestapp.py", "r")}

response = requests.post(url, files=f, data=user)
print(response.json())

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit-server'))
channel = connection.channel()

user = "user1"
results = channel.queue_declare(queue=user)
print(results)
f = open("worldwide_covid.json", "r") 
parsed_json = json.loads(f.read())
f.close() 

for item in parsed_json["records"]:
    response = channel.basic_publish(
                      exchange='',
                      routing_key=user,
                      body=json.dumps(item))

connection.close()

time.sleep(1000)

url = 'http://flask_service:80/stop'
user = {'user': 'user1'}

response = requests.post(url, data=user)
print(response.json())
