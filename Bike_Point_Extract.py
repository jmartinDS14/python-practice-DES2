import requests
import json
import os

url = 'https://api.tfl.gov.uk/BikePoint'
response = requests.get(url)

if response.status_code==200:
    #save the json response into a data variable
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

        file_list = [f for f in os.listdir('.') if f.endswith('.json')]

        if filename in file_list:
                print(bp+' up to date')
        else:
            #save to a file
            with open(filename,'w') as file:
                json.dump(bike_point,file)
else:
    #this bit goes and gets a cleaner error message
    data = response.json()
    error_message = data.get("message", "No message provided.")
    print(f'Error {response.status_code}: {error_message}')

