import json
import boto3

def lambda_handler(event, context):
    vote = json.loads(event['body'])['vote']

    print("Vote: " + vote)
    
    sns = boto3.client('sns', region_name='eu-central-1')

    response = sns.publish(
        TopicArn='arn:aws:sns:eu-central-1:971702022395:my-vote',
        Message=vote
    )
    
    return {
        'statusCode': 200,
        'body': '{"status": "success"}'
    }
