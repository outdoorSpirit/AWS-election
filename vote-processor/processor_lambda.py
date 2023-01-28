

import boto3
import json
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

queue = boto3.resource('sqs', region_name='us-east-1').get_queue_by_name(QueueName="erjan")
table = boto3.resource('dynamodb', region_name='us-east-1').Table('Votes')

def process_message(message):
    print('----------process_message----------------------')
    print('-------------SQS auto genereated msg------------------------')
    print(type(message))

    try:
        print('----------process_message----------------------')

        payload = message['messageAttributes']
        vote  = payload['vote']['stringValue']
        print('-----------------------------------------------')
        print('vote ' + str(vote))
        print('----------------------------------------')
        update_count(vote)
    except Exception as e:
        print('-----EXCEPTION-----')
        print(e)
        logging.info(sys.exc_info()[0])




def update_count(vote):
    print('update count....')
    cur_count = 0
    if vote == 'b':
        print('vote is b - update...')

        response = table.get_item(Key = {'voter':'count'})
        item = response['Item']
        item['b'] +=1
        table.put_item(Item = item)
            
    elif vote == 'a':
        print('vote is a - update...')
        
        table.update_item(
        Key={'voter':'count'},
        UpdateExpression="ADD a :incr",
        ExpressionAttributeValues={':incr': 1})



def lambda_handler(event,context):

    logging.info(event)
    logging.info(context)
    logging.info('--------inside main-------')
    
    print(event)
    print(context)
    print('--------inside main-------')

    try:
        print('--------------------------------------')
        print(event)
        print('------------------------inside try - queue.receive_messages-------------')
        message = event['Records'][0]

        try:
           
            process_message(message)
        except :
            print(' catch it here')


        return {'statusCode': 200, 'body': '{"status": "success"}'}

    except Exception as e:
       logging.error(e)
       logging.error(sys.exc_info()[0])
       return {'statusCode': 500, 'body': '{"status": "error"}'} 
