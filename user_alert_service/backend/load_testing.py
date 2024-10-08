import requests

while True:
    data = requests.get("http://localhost:8001/api/v1/health")
    print(data)