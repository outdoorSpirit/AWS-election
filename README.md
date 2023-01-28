# My Vote AWS

The application is already written, and all you have to do is deploy it using the technologies you have learned! The system is already familiar to you from the Infrastructure as a Code module, it is a demo application for voting, but this time it is redesigned to use the capabilities of AWS directly: it consists of two front-end components (JS Single-Page Application) and three back-end components ( Python).

We propose the following scheme: publish static files in S3 buckets (one for each frontend), host backends as Lambda functions and make them accessible using API Gateway. We suggest running the vote processor on EC2, although you may prefer pure serverless.

![Screenshot_31](https://user-images.githubusercontent.com/4441068/212905590-feb78ec6-16ba-428e-99bd-c08d3da777ac.png)


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


![Screenshot_31](https://user-images.githubusercontent.com/4441068/212555680-28762471-036b-4beb-af78-6c4e38e2276e.png)




For terraform, i used serverless lambda instead of ec2

![Screenshot_43](https://user-images.githubusercontent.com/4441068/215296208-a9f390c4-9d32-461e-8b46-0450a737b71f.png)

