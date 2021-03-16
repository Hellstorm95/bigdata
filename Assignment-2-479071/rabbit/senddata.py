import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit-server'))
channel = connection.channel()

user = "user1"
channel.queue_declare(queue=user)
f = open("worldwide_covid.json", "r") 
parsed_json = json.loads(f.read())
f.close() 

for item in parsed_json:
    channel.basic_publish(
                      exchange='',
                      routing_key=user,
                      body=item)
connection.close()
