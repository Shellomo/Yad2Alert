import json
import os
import boto3
from botocore import exceptions

bucket_name = os.getenv('BUCKETNAME')


def get_db_file(file_name, create=True):
    s3 = boto3.client('s3')
    # make sure bucket exists
    try:
        s3.head_bucket(Bucket=bucket_name)
    except exceptions.ClientError as e:
        print(e)
        exit(1)

    # make sure file exists
    try:
        s3.head_object(Bucket=bucket_name, Key=file_name)
    except exceptions.ClientError:
        if create:
            print('File does not exist. creating...')
            with open(file_name, 'w', encoding='utf8') as f:
                json.dump({}, f)
            return {}
        else:
            print(f'File {file_name} does not exist. exiting...')
            exit(1)

    s3.download_file(bucket_name, file_name, file_name)

    with open(file_name, 'r', encoding='utf8') as f:
        return json.load(f)


def put_db_file(file_name):
    s3 = boto3.client('s3')
    print('uploading file: ' + file_name)
    with open(file_name, 'r', encoding='utf8') as f:
        print(json.load(f))
    s3.upload_file(file_name, bucket_name, file_name)
