
import boto3
import logging
import sys
import os

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

region = os.environ.get("region")
sqs_queue_name = os.environ.get("sqs_queue_name")
dynamodb_table_name =  os.environ.get("dynamodb_table_name")
dynamodb_partition_key = os.environ.get("dynamodb_partition_key")
dynamodb_field = os.environ.get("dynamodb_field")

queue = boto3.resource('sqs', region_name=region).get_queue_by_name(QueueName=sqs_queue_name)
table = boto3.resource('dynamodb', region_name=region).Table(dynamodb_table_name)


def process_message(message):
    try:
        payload = message['messageAttributes']
        vote = payload[dynamodb_field]['stringValue']
        update_count(vote)
    except Exception as e:
        print('-----EXCEPTION-----')
        print(e)
        logging.info(sys.exc_info()[0])



def update_count(vote):
    print('update count....')    
    if vote == 'b':
        print('vote is b - update...')
        response = table.get_item(Key={dynamodb_partition_key: 'count'})
        item = response['Item']
        item['b'] += 1
        table.put_item(Item=item)

    elif vote == 'a':
        print('vote is a - update...')
        table.update_item(
            Key={dynamodb_partition_key: 'count'},
            UpdateExpression="ADD a :incr",
            ExpressionAttributeValues={':incr': 1})


def lambda_handler(event,context):
    logging.info('--------inside lambda handler-------')

    try:
        message = event['Records'][0]
        # messages = queue.receive_messages(MessageAttributeNames=[dynamodb_field, dynamodb_partition_key])
        
        process_message(message)
        return {'statusCode': 200, 'body': '{"status": "success"}'}

    except Exception as e:
       logging.error(e)
       logging.error(sys.exc_info()[0])
       return {'statusCode': 500, 'body': '{"status": "error"}'} 