import requests

url = "http://127.0.0.1:5000/api/device/state/air/13"

payload = "{\n\t\"value\": 10\n }"
headers = {'content-type': 'application/json'}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)