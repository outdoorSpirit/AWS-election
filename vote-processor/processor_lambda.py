

import boto3
import json
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

queue = boto3.resource('sqs', region_name='us-east-1').get_queue_by_name(QueueName="erjan")
table = boto3.resource('dynamodb', region_name='us-east-1').Table('Votes')

def process_message(message):
    try:
        payload = message['messageAttributes'] #message.messageAttributes
        vote  = payload['vote']['stringValue']       
        update_count(vote)
    except Exception as e:        
        logging.info(sys.exc_info()[0])




def update_count(vote):
    logging.info('update count....')
    cur_count = 0
    if vote == 'b':
        logging.info('vote is b - update...')

        response = table.get_item(Key = {'voter':'count'})
        item = response['Item']
        item['b'] +=1
        table.put_item(Item = item)
            
    elif vote == 'a':
        logging.info('vote is a - update...')
        
        table.update_item(
        Key={'voter':'count'},
        UpdateExpression="ADD a :incr",
        ExpressionAttributeValues={':incr': 1})



def lambda_handler(event,context):


    try:

        message = event['Records'][0]

        try:           
            process_message(message)
        except :
            print(' catch it here')
            
            # logging.info(sys.exc_info()[0])


     
        
        return {'statusCode': 200, 'body': '{"status": "success"}'}

    except Exception as e:
       logging.error(e)
       logging.error(sys.exc_info()[0])
       return {'statusCode': 500, 'body': '{"status": "error"}'} 
