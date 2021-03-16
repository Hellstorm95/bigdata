import requests
import json


url = 'http://flask_service:80/load_script'
user = {'user': 'user1'}
f = {"file": open("clientbatchingestapp.py", "r")}

response = requests.post(url, files=f, data=user)
data = response.json()

print(response)
print(data)

url = 'http://flask_service:80/ingest_files'
user = {'user': 'user1'}
f = {
    "file": open("worldwide_covid.json", "r"), 
}

response = requests.post(url, files=f, data=user)
data = response.json()


print(response)
print(data)
