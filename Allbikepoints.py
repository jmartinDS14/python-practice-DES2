import requests
import json
import os

url = 'https://api.tfl.gov.uk/BikePoint'
response = requests.get(url)

data = response.json()
number_of_bike_points = len([item.get('id') for item in data])

for i in range(0,number_of_bike_points):
    bike_point = data[i]

    first_value = bike_point['additionalProperties'][0]
    modified = first_value.get('modified')
    modified = modified.replace(':','-')
    modified = modified.replace('.','-')

    bp = bike_point.get('id')

    filename = modified+bp+'.json'

    with open(filename,'w') as file:
        json.dump(bike_point,file)