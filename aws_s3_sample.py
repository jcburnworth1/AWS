##### Import Libraries #####
import os
import boto3

## Environment Variables
AWS_KEY_ID = os.environ['access_key_id']
SECRET_ACCESS_KEY = os.environ['secret_access_key']
REGION = os.environ['region']

## Setup S3 Client
s3 = boto3.client('s3',
                  region_name=REGION,
                  aws_access_key_id=AWS_KEY_ID,
                  aws_secret_access_key=SECRET_ACCESS_KEY,
                  verify=False)

## Create Bucket
bucket = s3.create_bucket(Bucket='gid-requests-jc')
print(bucket)

## List Buckets
buckets = s3.list_buckets()

## Upload file to Bucket
s3.upload_file(Bucket='gid-requests-jc',
               Filename='Account_20200305.txt',
               Key='Account_20200305.txt')

## Head Objects
contents = s3.head_object(Bucket='gid-requests-jc',
                          Key='Account_20200305.txt')
print(contents)

## List Objects
contents = s3.list_objects(Bucket='gid-requests-jc') # can add Prefix= for regex style search

## Remove file
s3.delete_object(Bucket='gid-requests-jc',
                 Key='Account_20200305.txt')

## Delete Bucket
bucket = s3.delete_bucket(Bucket='gid-requests-jc')
print(bucket)