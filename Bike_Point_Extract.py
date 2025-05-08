import requests
import json
import os

url = 'https://api.tfl.gov.uk/BikePoint'
response = requests.get(url)

if response.status_code==200:
    #save the json response into a data variable
    data = response.json()
    id = [item.get('id') for item in data]

    for bp in id:
        endpoint = url + '/' + bp
        endpoint_response = requests.get(endpoint)
        endpoint_data = endpoint_response.json()
    
        #get modified timestamp to help us name our file
        first_value = endpoint_data['additionalProperties'][0]
        modified = first_value.get('modified')
        modified = modified.replace(':','-')
        modified = modified.replace('.','-')
        #print(modified)

        file_list = [f for f in os.listdir('.') if f.endswith('.json')]
        #print(file_list)

        filename = modified+bp+'.json'
        #print(filename)

        if filename in file_list:
            print('Up to date')
        else:
            #save to a file
            with open(filename,'w') as file:
                json.dump(endpoint_data,file)

else:
    #this bit goes and gets a cleaner error message
    data = response.json()
    error_message = data.get("message", "No message provided.")
    print(f'Error {response.status_code}: {error_message}')

