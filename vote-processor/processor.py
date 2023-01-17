#!/usr/bin/env python3

import boto3
import json
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

queue = boto3.resource('sqs', region_name='us-east-1').get_queue_by_name(QueueName="erjan")
table = boto3.resource('dynamodb', region_name='us-east-1').Table('Votes')

def process_message(message):
    try:
        payload = message.message_attributes
        voter = payload['voter']['StringValue']
        vote  = payload['vote']['StringValue']
        #store_vote(voter,vote)
        logging.info("Voter: %s, Vote: %s", voter, vote)
        update_count(vote)
        message.delete()
    except Exception as e:
        print('-----EXCEPTION-----')

def store_vote(voter, vote):
    try:
        logging.info('table put item.......')

        #here is the error i had! i WAS PUTTING THIS THING INTO TABLE - REWRITING MY OWN 'A' AND 'B'
        response = table.put_item(
           Item={'voter': voter, 'vote': vote}
        )
    except:
        logging.error("Failed to store message")
        raise

def update_count(vote):
    logging.info('update count....')
    cur_count = 0
    if vote == 'b':
        response = table.get_item(Key = {'voter':'count'})
        item = response['Item']
        item['b'] +=1
        table.put_item(Item = item)
            
    elif vote == 'a':
        table.update_item(
        Key={'voter':'count'},
        UpdateExpression="ADD a :incr",
        ExpressionAttributeValues={':incr': 1})

if __name__ == "__main__":

    logging.info('--------inside main-------')

    while True:
        try:
            messages = queue.receive_messages(MessageAttributeNames=['vote','voter'])
            #messages = queue.receive_messages()
        except KeyboardInterrupt:
           logging.info("Stopping...")
           break
        except:
            logging.error(sys.exc_info()[0])
            continue
        for message in messages:
            process_message(message)
