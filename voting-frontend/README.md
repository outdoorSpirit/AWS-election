# Voting Frontend

The frontend consists of a primitive javascript application. Create a bucket and set it up for hosting a website, as we already did. Optionally, you can use CloudFront if you prefer a more complex task. In this case, to deploy files, you will need to invalidate the CloudFront cache.

## Deploy

Substitute your bucket name in the file upload command. Files can also be uploaded manually, but I recommend getting used to AWS Cli. In the 28th line of the [index.html](./index.html#L28) file, correct the path to the backend - this will be the address of the API Gateway ([hints here](../gateway)).

```
cd voting-frontend
aws s3 cp . s3://VOTINGBUCKETNAME --recursive --acl public-read
```



## sample bucket policy for s3 vote - integration with cloudfront
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::frontend-erjan-vote/*"
        },
        {
            "Sid": "S3PolicyStmt-DO-NOT-MODIFY-1673091928784",
            "Effect": "Allow",
            "Principal": {
                "Service": "logging.s3.amazonaws.com"
            },
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::frontend-erjan-vote/*"
        },
        {
            "Sid": "3",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity E2NHXOJ7VCG7IJ"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::frontend-erjan-vote/*"
        }
    ]
}
```
