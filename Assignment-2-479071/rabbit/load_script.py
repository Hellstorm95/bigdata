import requests
import json


url = 'flask_service/start'
user = {'user': 'test1'}
f = {"file": open("clientstreamingestapp.py", "r")}

response = requests.post(url, files=f, data=user)
data = response.json()

print(response)
print(data)
tag = data['tag']

url = 'http://0.0.0.0:56733/stop'
user = {'user': 'test1', 'tag': tag}

response = requests.post(url, data=user)
data = response.json()


print(response)
print(data)
