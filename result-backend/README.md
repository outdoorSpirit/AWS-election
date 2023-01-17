# Results Backend

Lambda function available to the frontend via API Gateway. The proposed code is given in the file.


IAM policy and role to be attached to the lambda should look like this:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "dynamodb:DeleteItem",
                "dynamodb:GetShardIterator",
                "dynamodb:GetItem",
                "dynamodb:DescribeStream",
                "dynamodb:GetRecords"
            ],
            "Resource": "arn:aws:dynamodb:us-east-1:025416187662:table/Votes"
        }
    ]
}
```
