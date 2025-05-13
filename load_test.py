import boto3
import os
from dotenv import load_dotenv

def load_to_s3(filename):

    load_dotenv()

    access_key = os.getenv('AWS_ACCESS_KEY')
    secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    bucket = os.getenv('AWS_BUCKET_NAME')

    s3_client = boto3.client(
        's3',
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_access_key
    )

    s3_client.upload_file(filename,bucket,filename)

load_dotenv()

access_key = os.getenv('AWS_ACCESS_KEY')
secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
bucket = os.getenv('AWS_BUCKET_NAME')

s3_client = boto3.client(
    's3',
    aws_access_key_id = access_key,
    aws_secret_access_key = secret_access_key
)


file_list = s3_client.list_objects_v2(Bucket=bucket)
files = [item['Key'] for item in file_list.get('Contents', [])]

print(files)