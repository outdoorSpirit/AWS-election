import logging
import boto3

logging.getLogger().setLevel(logging.INFO)

def lambda_handler(event, context):
    dynamodb = boto3.client('dynamodb')
    count = dynamodb.get_item(TableName='Votes', Key={'voter':{'S': 'count'}})
    
    a = count["Item"]["a"]["N"]
    b = count["Item"]["b"]["N"]

    return {'statusCode': 200, 'body': '{"a": ' + a + ', "b": ' + b + '}'}
