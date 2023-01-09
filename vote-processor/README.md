# Vote Processor

Vote Processor must be running on EC2 facilities. Choose one of the options:

* Separate EC2 Instance
* Launch Template + Target Group
* Autoscaling Group (on-demand)
* Autoscaling Group (spot/on-demand)

**Please note** that in the 11th and 12th lines of the handler, you must specify the correct SQS queue and DynamoDB table.

## Recommended configuration

*Amazon Linux 2
*T2.Micro

## Local Run
```
python -m pip install --user boto3
chmod +x processor.py
./processor.py
```

## Run on EC2 instance (User Data)
```
#!/bin/bash
curl https://raw.githubusercontent.com/erjan/MyVoteAWS/main/vote-processor/processor.py > processor.py
chmod +x processor.py
yum -y install python-pip
python -m pip install --user boto3
./processor.py
```

### Policy for SQS

```
{
     "Version": "2012-10-17",
     "Statement": [
         {
             "Effect": "Allow",
             "Action": [
                 "sqs:GetQueueUrl",
                 "sqs:ReceiveMessage",
                 "sqs:DeleteMessage"
             ],
             "Resource": "arn:aws:sqs:*:ACCOUNT:QUEUENAME"
         }
     ]
}
```

### Policy for DynamoDB

```
{
     "Version": "2012-10-17",
     "Statement": [
         {
             "Effect": "Allow",
             "Action": [
                 "dynamodb:PutItem",
                 "dynamodb:UpdateItem"
             ],
             "Resource": "arn:aws:dynamodb:*:ACCOUNT:table/TABLENAME"
         }
     ]
}
```
