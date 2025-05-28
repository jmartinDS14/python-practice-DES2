import requests
import json
import os
import boto3
from dotenv import load_dotenv
from load_test import load_to_s3

load_dotenv()

access_key = os.getenv('AWS_ACCESS_KEY')
secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
bucket = os.getenv('AWS_BUCKET_NAME')
print("Bucket:", bucket)

s3_client = boto3.client(
    's3',
    aws_access_key_id = access_key,
    aws_secret_access_key = secret_access_key
)

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

        s3_contents = s3_client.list_objects_v2(Bucket=bucket)
        file_list = [item['Key'] for item in s3_contents.get('Contents', [])]

        if filename in file_list:
            print(bp+' up to date')
        else:
            #save to a file
            with open(filename,'w') as file:
                json.dump(bike_point,file)
            load_to_s3(filename)
            print('Uploaded '+filename)
else:
    #this bit goes and gets a cleaner error message
    data = response.json()
    error_message = data.get("message", "No message provided.")
    print(f'Error {response.status_code}: {error_message}')

