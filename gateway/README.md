API Gateways
Try to configure the API Gateway yourself using the knowledge from the recent module. Tips can be seen below.

CORS Settings
Cross-Origin request settings. Please note that both GET and POST requests (to record a vote and get results) are allowed, and two request sources are connected: my-vote (voting) and my-vote-result (results).

![image](https://user-images.githubusercontent.com/1742301/106400513-1b512a80-641f-11eb-8a07-c05b55ca3857.png)

## Routes

In this example, I used one path `/my-vote`, and made the routing based on the request method `GET`/`POST`. This is not mandatory, you can do two different ways.

![image](https://user-images.githubusercontent.com/1742301/106399262-dfff2d80-6417-11eb-9222-45eea37637e2.png)

## Integrations

This API must support two functions from AWS Lambda as integrations. This repository contains their code:

* [Бэкенд голосованя](../voting-backend)
* [Бэкенд результатов](../result-backend)
