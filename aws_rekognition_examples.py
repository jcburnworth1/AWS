##### Import Libraries #####
import os
import boto3

##### Environment Variables #####
AWS_KEY_ID = os.environ['access_key_id']
SECRET_ACCESS_KEY = os.environ['secret_access_key']
REGION = os.environ['region']

##### Setup Rekognition Client #####
rekog = boto3.client('rekognition',
                     region_name=REGION,
                     aws_access_key_id=AWS_KEY_ID,
                     aws_secret_access_key=SECRET_ACCESS_KEY,
                     verify=False)

##### Basics #####
## Detect Image
image_response = rekog.detect_labels(Image={'S3Object': {'Bucket': 'bucket-img-jc',
                                                         'Name': 'test.jpg'}
                                            },
                                     MaxLabels=10,
                                     MinConfidence=95)

## Detect Text
text_response = rekog.detect_text(Image={'S3Object': {'Bucket': 'bucket-img-jc',
                                                      'Name': 'test.jpg'}
                                         })
