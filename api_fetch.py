import requests
import json

url = 'http://localhost:5000/api/crop-recommendation'
data = {
    'N': 10,
    'P': 18,
    'K': 30,
    'temperature': 23.603016,
    'humidity': 140.91,
    'ph': 6.7,
    'rainfall': 150.9
}
headers = {'Content-type': 'application/json'}

response = requests.get(url, json=data, headers=headers)
if response.status_code == 200:
    data = response.json()
    # Process the response data
    print(data)
else:
    print(f'Request failed with status code {response.status_code}')