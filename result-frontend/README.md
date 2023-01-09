# Result Frontend

The results frontend is very similar to the voting frontend and is a primitive SPA application. Create another bucket and set it up to host the website, as we did before. Optionally, you can use CloudFront if you prefer a more complex task. In this case, to deploy files, you will need to invalidate the CloudFront cache.

Important In the 17th line of the file, change the path to the backend to the appropriate one. To get results, the API Gateway must support GET requests to the voting results backend.

## Deploy

Substitute your bucket name in the file upload command. Files can also be uploaded manually, but I recommend getting used to AWS Cli. In the 17th line of the app.js file, correct the path to the backend - this will be the address of the API Gateway (hints here).

```
cd result-frontend
aws s3 cp . s3://RESULTBUCKETNAME --recursive --acl public-read
```
