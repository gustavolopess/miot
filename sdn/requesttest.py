import requests

url = "http://10.0.0.1:5000/api/device/state/air/1/"

payload = "{\n\t\"value\": 7.9\n}"
headers = {'content-type': 'application/json'}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)