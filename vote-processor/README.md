# Запуск

## Локальный Запуск
```
python -m pip install --user boto3
chmod +x processor.py
./processor.py
```

## Запуск на инстансе EC2 (User Data)
```
#!/bin/bash
curl https://raw.githubusercontent.com/HadesArchitect/MyVoteAWS/main/vote-processor/processor.py > processor.py
chmod +x processor.py
yum -y install python-pip
python -m pip install --user boto3
./processor.py
```

# Зависимости

## Политики

### Политика для SQS

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

### Политика для DynamoDB

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
             "Effect": "Allow",
            "Action": "dynamodb:PutItem",
            "Resource": "arn:aws:dynamodb:*:ACCOUNT:table/TABLENAME"
        }
    ]
}
```