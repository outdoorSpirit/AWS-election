import json
import sys
import logging
import boto3

logging.getLogger().setLevel(logging.INFO)

def lambda_handler(event, context):
    #vote = json.loads(event['body'])['vote']
    
    payload = event['body'] #json.loads(message.body)
    voter = payload['MessageAttributes']['voter']['Value']
    vote  = payload['MessageAttributes']['vote']['Value']
    print('---------------------------------------------------------------------')
    print('---------------------------------------------------------------------')
    print('---------------------------------------------------------------------')
    print('---------------------------------------------------------------------')
    
    # vote = event['Records'][0]['Sns']['MessageAttributes']['vote']['Value']

    # vote = x['vote']
    # voter = 'default_voter'

    logging.info('****Vote: %s, Voter: %s', vote, voter)
    
    try:
        publish_vote(vote, voter)
    except:
        e = sys.exc_info()[0]
        logging.error(e)
        return {'statusCode': 500, 'body': '{"status": "error"}'} 
    
    return {'statusCode': 200, 'body': '{"status": "success"}'}

def publish_vote(vote, voter):
    sns = boto3.client('sns', region_name='us-east-1')
    logging.info('starting sending vote to SNS topic XXXXXXXXX')

    sns.publish(
        TopicArn='arn:aws:sns:us-east-1:025416187662:erjan',
        Message='""',
        MessageAttributes={
            "vote": {
                "DataType": "String",
                "StringValue": vote,
            },
            "voter": {
                "DataType": "String",
                "StringValue": voter,
            }          
        }
    )
    logging.info('XXXX XXXXXX ***** message published')
