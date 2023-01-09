# Voting Frontend

The frontend consists of a primitive javascript application. Create a bucket and set it up for hosting a website, as we already did. Optionally, you can use CloudFront if you prefer a more complex task. In this case, to deploy files, you will need to invalidate the CloudFront cache.

## Deploy

Substitute your bucket name in the file upload command. Files can also be uploaded manually, but I recommend getting used to AWS Cli. In the 28th line of the [index.html](./index.html#L28) file, correct the path to the backend - this will be the address of the API Gateway ([hints here](../gateway)).

```
cd voting-frontend
aws s3 cp . s3://VOTINGBUCKETNAME --recursive --acl public-read
```
