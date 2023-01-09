# My Vote AWS

AWS Slurm DIY Materials (Basic). The application is already written, and all you have to do is deploy it using the technologies you have learned! The system is already familiar to you from the Infrastructure as a Code module, it is a demo application for voting, but this time it is redesigned to use the capabilities of AWS directly: it consists of two front-end components (JS Single-Page Application) and three back-end components ( Python).

We propose the following scheme: publish static files in S3 buckets (one for each frontend), host backends as Lambda functions and make them accessible using API Gateway. We suggest running the voice processor on EC2, although you may prefer pure serverless.

![image](https://user-images.githubusercontent.com/1742301/106404317-b9022500-6432-11eb-94ed-602d2b27b8fb.png)

Note that while all the code has already been written, you still have a lot of work to do in creating resources (queues, DynamoDB tables) and assigning access to them. If necessary, use the hints located in the appropriate folders.

## Used tech

* ✅ EC2
* ✅ S3
* ✅ CloudFront
* ✅ database (DynamoDB)
* ✅ VPC
* ✅ SQS queue
* ✅ SNS notifications
* ✅ Serverless (API Gateway, Lambda)
* ✅ IAM

Challenge:
* ⚠️ IaaC (Terraform, CloudFormation, Cloud Development Kit)
* ⚠️ Billing и Costs

## Components

* [API Gateway](./gateway)
* [voting frontend, Javascript](./voting-frontend)
* [voting backend, Python](./voting-backend)
* [vote processor, Python](./vote-processor)
* [database, DynamoDB](./dynamodb)
* [result backend, Python](./result-backend)
* [result frontend, Javascript](./result-frontend)

## Architecture


![Screenshot_21](https://user-images.githubusercontent.com/4441068/210948938-036bd569-41ed-4752-b1f0-afa3258d7f73.png)
