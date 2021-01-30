import json
import sys
import logging
import boto3

logging.getLogger().setLevel(logging.DEBUG)

def lambda_handler(event, context):
    vote = json.loads(event['body'])['vote']
    voter = 'default_voter'

    logging.info('Vote: %s, Voter: %s', vote, voter)
    
    try:
        publish_vote(vote, voter)
    except:
        e = sys.exc_info()[0]
        logging.error(e)
        return {'statusCode': 500, 'body': '{"status": "error"}'} 
    
    return {'statusCode': 200, 'body': '{"status": "success"}'}

def publish_vote(vote, voter):
    sns = boto3.client('sns', region_name='eu-central-1')
    sns.publish(
        TopicArn='arn:aws:sns:eu-central-1:971702022395:my-vote',
        Message='""',
        MessageAttributes={
            'vote': {
                'DataType': 'String',
                'StringValue': vote,
            },
            'voter': {
                'DataType': 'String',
                'StringValue': voter,
            }          
        }
    )
    logging.info('message published')
