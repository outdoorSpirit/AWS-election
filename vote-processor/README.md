# Vote Processor

Vote Processor должен быть запущен на мощностях EC2. Выберите один из вариантов:

* Отдельный Инстанс EC2
* Launch Template + Target Group
* Autoscaling Group (on-demand)
* Autoscaling Group (spot/on-demand)

**Обратите внимание**, что в 11-той и 12-той строчках обработчика надо указать верные очередь SQS и таблицу DynamoDB.

## Рекомендуемая конфигурация

* Amazon Linux 2
* T2.Micro

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
            "Action": [
                "dynamodb:PutItem",
                "dynamodb:UpdateItem"
            ],
            "Resource": "arn:aws:dynamodb:*:ACCOUNT:table/TABLENAME"
        }
    ]
}
```
