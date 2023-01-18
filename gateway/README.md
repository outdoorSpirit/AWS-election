## API Gateways

Try to configure the API Gateway yourself using the knowledge from the recent module. Tips can be seen below.

## CORS Settings
Cross-Origin request settings. Please note that both GET and POST requests (to record a vote and get results) are allowed, and two request sources are connected: my-vote (voting) and my-vote-result (results).

Notice how accepted origins are not s3 buckets - but only 2 cloudfronts!

![Screenshot_8](https://user-images.githubusercontent.com/4441068/213271979-4f02d074-434b-4dc0-ab67-d68e54af215c.png)


## Routes

In this example, I used one path `/my-vote`, and made the routing based on the request method `GET`/`POST`. This is not mandatory, you can do two different ways.


![Screenshot_40](https://user-images.githubusercontent.com/4441068/213276723-545166c8-a51d-4d75-9769-cb590d7c8477.png)


## Integrations

This API must support two functions from AWS Lambda as integrations. This repository contains their code:

* [Бэкенд голосования](../voting-backend)
* [Бэкенд результатов](../result-backend)
