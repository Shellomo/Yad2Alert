import json

import boto3
from botocore import exceptions
# import settings
import settings_temp as settings  # ToDo: remove this


def get_db_file(file_name):
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    # make sure bucket exists
    try:
        s3.head_bucket(Bucket=settings.BUCKET_NAME)
    except exceptions.ClientError:
        print('Bucket does not exist.\nExiting...')
        exit(1)

    # make sure file exists
    try:
        s3.head_object(Bucket=settings.BUCKET_NAME, Key=file_name)
    except exceptions.ClientError:
        print('File does not exist. creating...')
        with open(file_name, 'w', encoding='utf8') as f:
            json.dump({}, f)
        return {}

    s3.download_file(settings.BUCKET_NAME, file_name, file_name)

    with open(file_name, 'r', encoding='utf8') as f:
        print('found file: ' + file_name)
        print(json.load(f))
        return json.load(f)


def put_db_file(file_name):
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    print('uploading file: ' + file_name)
    with open(file_name, 'r', encoding='utf8') as f:
        print(json.load(f))
    s3.upload_file(file_name, settings.BUCKET_NAME, file_name)
