import json
import sys
import logging
import boto3

logging.getLogger().setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        logging.info(event)
        
        payload = event["body"]
        print('----------------------------------')
        print('event')
        print(event)
        print('event type')
        print(type(event))
        try:
            print('---------------------------------------------')
            print(payload)
        except Exception as e:
            print(e)
            
        print('---------------------------------------------------')
        print('---------------------------------------------------------')
        res = json.loads(payload)
        print('--------------RES-----------------')
        print(res)
        print()
        voter = res["MessageAttributes"]["voter"]["StringValue"] # this is good only for test event 
        vote  = res["MessageAttributes"]["vote"]["StringValue"]
        
        # voter = res['MessageAttributes']['voter']['StringValue']
        # vote  = res['MessageAttributes']['vote']['StringValue']
        # print('-------------VOTER----------------')
        # print('-------------------------------')
        # print(voter)
        # print(vote)
        
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
    logging.info('                                              MSG PUBLISHED - SUCCESS')
