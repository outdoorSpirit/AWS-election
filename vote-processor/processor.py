#!/usr/bin/env python

import boto3
import json
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

queue = boto3.resource("sqs").get_queue_by_name(QueueName="my-vote")
table = boto3.resource('dynamodb', region_name='eu-central-1').Table('Votes')

def process_message(message):
    try:
        payload = json.loads(message.body)
        voter = payload['MessageAttributes']['voter']['Value']
        vote  = payload['MessageAttributes']['vote']['Value']
        logging.info("Voter: %s, Vote: %s", voter, vote)
        store_vote(voter, vote)
        message.delete()
    except:
        logging.error(sys.exc_info()[0])

def store_vote(voter, vote):
    response = table.put_item(
       Item={
            'voter': voter,
            'vote': vote,
        }
    )

if __name__ == "__main__":
    while True:
        try:
            messages = queue.receive_messages()
        except:
            logging.error(sys.exc_info()[0])
            continue
        for message in messages:
            process_message(message)
