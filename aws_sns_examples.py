##### Import Libraries #####
import os
import boto3

##### Environment Variables #####
AWS_KEY_ID = os.environ['access_key_id']
SECRET_ACCESS_KEY = os.environ['secret_access_key']
REGION = os.environ['region']
TOPIC = 'city_alerts'
TOPICARN = None

##### Setup SNS Client #####
sns = boto3.client('sns',
                   region_name=REGION,
                   aws_access_key_id=AWS_KEY_ID,
                   aws_secret_access_key=SECRET_ACCESS_KEY,
                   verify=False)

##### Basics #####
## Create Topic
create_topic_response = sns.create_topic(Name='city_alerts')

if create_topic_response['ResponseMetadata']['HTTPStatusCode'] == 200:
    print(f"Topic Successfully Created - Topic ARN: {create_topic_response['TopicArn']}")
    TOPICARN=create_topic_response['TopicArn']

## List Topics
list_topic_response = sns.list_topics()

## Delete Topics
delete_response = sns.delete_topic(TopicArn=TOPICARN)

##### Manage Topic Subscriptions #####
## Create subscription
create_sub_response = sns.subscribe(TopicArn=TOPICARN,
                                    Protocol='sms', #email - requires confirmation
                                    Endpoint='+13148675309') #jcburnworth@yahoo.com

## List Subscriptions by Topic
list_subs_response = sns.list_subscriptions_by_topic(TopicArn=TOPICARN)
SUBSCRIPTIONARN = list_subs_response['Subscriptions'][0]['SubscriptionArn']

## Delete Subscription
delete_sub_response = sns.unsubscribe(
    SubscriptionArn=SUBSCRIPTIONARN)

## Delete Multiple Subscriptions
list_subs_response = sns.list_subscriptions_by_topic(TopicArn=TOPICARN)

for sub in list_subs_response['Subscriptions']:
    if sub['Protocol'] == 'sms':
        sns.unsubscribe(SubscriptionArn=sub['SubscriptionArn'])

##### Sending Messages #####
## Publish Message to Topic
publish_response = sns.publish(TopicArn=TOPICARN,
                               Message='This is a Test',
                               Subject='This is a Test')