##### Import Libraries #####
import os
import boto3

##### Environment Variables #####
AWS_KEY_ID = os.environ['access_key_id']
SECRET_ACCESS_KEY = os.environ['secret_access_key']
REGION = os.environ['region']

##### Setup Translate Client #####
comprehend = boto3.client('comprehend',
                          region_name=REGION,
                          aws_access_key_id=AWS_KEY_ID,
                          aws_secret_access_key=SECRET_ACCESS_KEY,
                          verify=False)

##### Basics #####
## Translate
translate_response = comprehend.detect_dominate_language(Text='Hay basura por todas partes a lo largo de la carretera.')

## Sentiment Analysis
sentiment_response = comprehend.detect_sentiment(Text='I am not happy.')