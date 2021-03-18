import requests
import json


url = 'http://flask_service:80/load_script'
user = {'user': 'user2'}
f = {"file": open("clientbatchingestapp.py", "r")}

response = requests.post(url, files=f, data=user)
data = response.json()

print(response)
print(data)

url = 'http://flask_service:80/ingest_files'
user = {'user': 'user2'}
f = {
    "file": open("worldwide_covid.csv", "r"), 
    "file2": open("worldwide_covid.csv", "r"), 
    "file3": open("worldwide_covid.csv", "r"), 
    "file4": open("worldwide_covid.csv", "r"),
    "file5": open("worldwide_covid.csv", "r"),
}

response = requests.post(url, files=f, data=user)
data = response.json()

print(response)
print(data)
