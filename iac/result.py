
import logging
import boto3
import os
logging.getLogger().setLevel(logging.INFO)

dynamodb_table_name =  os.environ.get("dynamodb_table_name")
dynamodb_partition_key = os.environ.get("dynamodb_partition_key")

def lambda_handler(event, context):

    dynamodb = boto3.client('dynamodb')
    count = dynamodb.get_item(TableName=dynamodb_table_name, Key={dynamodb_partition_key: {'S': 'count'}})

    a = count["Item"]["a"]["N"]
    b = count["Item"]["b"]["N"]
    print("a: " + str(a))
    print("b: " + str(b))

    return {'statusCode': 200, 'body': '{"a": ' + a + ', "b": ' + b + '}'}
