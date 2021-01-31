import json
import logging
import boto3

logging.getLogger().setLevel(logging.INFO)

def lambda_handler(event, context):

#    try:
#        get_votes()
#    except Exception as e:
#        logging.error(e)
#        return {'statusCode': 500, 'body': '{"status": "error"}'} 
    
    return {'statusCode': 200, 'body': '{"a": 3, "b": 5}'}
