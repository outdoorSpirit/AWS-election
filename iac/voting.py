import json
import sys
import logging
import boto3
import os
logging.getLogger().setLevel(logging.INFO)

SNS_ARN = os.environ.get("SNS_ARN")
def_region = os.environ.get("def_region")

def lambda_handler(event, context):
    print('----------------------------------------HERE--------------------')
    logging.info('----------------------------------------HERE--------------------')
    try:
        logging.info(event)

        payload = event["body"]

        try:
            print('---------------------------------------------')
            print(payload)
        except Exception as e:
            print(e)
        res = json.loads(payload)
        # this is good only for test event
        voter = res["MessageAttributes"]["voter"]["StringValue"]
        vote = res["MessageAttributes"]["vote"]["StringValue"]
        publish_vote(vote, voter)

    except:
        e = sys.exc_info()[0]
        logging.error(e)
        return {'statusCode': 500, 'body': '{"status": "error"}'}

    return {'statusCode': 200, 'body': '{"status": "success"}'}


def publish_vote(vote, voter):
    sns = boto3.client('sns', region_name=def_region)

    sns.publish(
        TopicArn=SNS_ARN,
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
    logging.info('   MSG PUBLISHED - SUCCESS')
