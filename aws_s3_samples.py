##### Import Libraries #####
import os
import boto3
import pandas as pd

##### Environment Variables #####
AWS_KEY_ID = os.environ['access_key_id']
SECRET_ACCESS_KEY = os.environ['secret_access_key']
REGION = os.environ['region']
BUCKET = 'gid-requests-jc'
FILENAME = 'Account_20200305.txt'

##### Setup S3 Client #####
s3 = boto3.client('s3',
                  region_name=REGION,
                  aws_access_key_id=AWS_KEY_ID,
                  aws_secret_access_key=SECRET_ACCESS_KEY,
                  verify=False)

##### Basics #####
## Create Bucket
bucket = s3.create_bucket(Bucket=BUCKET)

if bucket['ResponseMetadata']['HTTPStatusCode'] == 200:
    print(f"Bucket Successfully Created: s3:/{bucket['Location']}")

## List Buckets
buckets = s3.list_buckets()

## Upload File to Bucket
s3.upload_file(Bucket=BUCKET,
               Filename=FILENAME,
               Key=FILENAME)

## Head Objects
contents = s3.head_object(Bucket=BUCKET,
                          Key=FILENAME)
print(contents)

## List Objects
contents = s3.list_objects(Bucket=BUCKET) # can add Prefix= for regex style search

## Remove File
s3.delete_object(Bucket=BUCKET,
                 Key=FILENAME)

## Delete Bucket
bucket = s3.delete_bucket(Bucket=BUCKET)
print(bucket)

##### S3 Object Access #####
## Upload File
s3.upload_file(Bucket=BUCKET,
               Filename=FILENAME,
               Key=FILENAME)

## Set ACL to `public-read`
# Access via https://{bucket}.s3.amazonaws.com/{key}
s3.put_object_acl(Bucket=BUCKET,
                  Key=FILENAME,
                  ACL='public-read')

## Upload and Access Set all in on
s3.upload_file(Bucket=BUCKET,
               Filename=FILENAME,
               Key=FILENAME,
               ExtraArgs={'ACL':'public-read'})

## Pre-signed URLs
share_url = s3.generate_presigned_url(ClientMethod='get_object',
                                      ExpiresIn=3600,
                                      Params={'Bucket':BUCKET,
                                              'Key':FILENAME})

## Loop Load Data from Private File
response = s3.list_objects(Bucket=BUCKET)
request_files = response['Contents']

account_df_list = []
for file in request_files:
    # For each file in response load the object from S3
    obj = s3.get_object(Bucket=BUCKET, Key=file['Key'])
    # Load the object's StreamingBody with pandas
    obj_df = pd.read_csv(obj['Body'], delimiter=';')
    # Append the resulting DataFrame to list
    account_df_list.append(obj_df)

# Concat all the DataFrames with pandas
account_df = pd.concat(account_df_list)

# Preview the resulting DataFrame
account_df.head()

##### S3 Object HTML #####
## Output HTML version of data frame
account_df.to_html('account_data.html',
                   render_links=True,
                   columns=['Account_Type','Account_Name'],
                   border=1)

## Send HTML data frame to S3
s3.upload_file(Bucket=BUCKET,
               Filename='account_data.html',
               Key='table.html',
               ExtraArgs={'ContentType':'text/html',
                          'ACL':'public-read'})

## Send Image to S3
s3.upload_file(Bucket=BUCKET,
               Filename='account_data.png',
               Key='plot_image.png')

## Generate an Index Page
## List Objects
response = s3.list_objects(Bucket=BUCKET)

## Convert response to data frame
objects_df = pd.DataFrame(response['Contents'])

## Create a column "Link" that contains website url + key
# https://s3.console.aws.amazon.com/s3/buckets/gid-requests-jc/?region=us-east-1
base_url = 'https://gid-requests-jc.s3.amazonaws.com/'
objects_df['Link'] = base_url + objects_df['Key']

## Output HTML version of data frame
objects_df.to_html('account_listing.html',
                   render_links=True,
                   columns=['Link','LastModified','Size'],
                   border=1)

## Upload Indexing Page
s3.upload_file(Bucket=BUCKET,
               Filename='account_listing.html',
               Key='index.html',
               ExtraArgs={'ContentType':'text/html',
                          'ACL':'public-read'})