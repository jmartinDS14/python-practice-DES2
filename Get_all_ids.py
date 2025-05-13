import requests

url = 'https://api.tfl.gov.uk/BikePoint'

response = requests.get(url)
data = response.json()

id = [item.get('id') for item in data]

for i in id:
    print(i)
