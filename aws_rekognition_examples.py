##### Import Libraries #####
import os
import boto3

##### Environment Variables #####
AWS_KEY_ID = os.environ['access_key_id']
SECRET_ACCESS_KEY = os.environ['secret_access_key']
REGION = os.environ['region']

##### Setup S3 Client #####
sns = boto3.client('rekognition',
                   region_name=REGION,
                   aws_access_key_id=AWS_KEY_ID,
                   aws_secret_access_key=SECRET_ACCESS_KEY,
                   verify=False)