from aws_cdk import (
    aws_cloudfront as cloudfront,
    aws_ec2 as ec2,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_dynamodb as dynamodb,
    aws_apigatewayv2 as apigatewayv2,
    aws_sns as sns,
    aws_sqs as sqs,
    aws_iam as iam,
    core as cdk
)

class MyStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        cloudfrontdistribution = cloudfront.CfnDistribution(
            self,
            "CloudFrontDistribution",
            distribution_config={
                "origins": [
                    {
                        "connection_attempts": 3,
                        "connection_timeout": 10,
                        "domain_name": "frontend-erjan-result.s3.us-east-1.amazonaws.com",
                        "id": "frontend-erjan-result.s3.us-east-1.amazonaws.com",
                        "origin_path": "",
                        "s3_origin_config": {
                            "origin_access_identity": "origin-access-identity/cloudfront/E36TPZ2E5JVKVL"
                        }
                    }
                ],
                "default_cache_behavior": {
                    "allowed_methods": [
                        "HEAD",
                        "GET",
                        "OPTIONS"
                    ],
                    "cached_methods": [
                        "HEAD",
                        "GET",
                        "OPTIONS"
                    ],
                    "compress": True,
                    "cache_policy_id": "658327ea-f89d-4fab-a63d-7e88639e58f6",
                    "origin_request_policy_id": "88a5eaf4-2fd4-4709-b370-b4c650ea3fcf",
                    "response_headers_policy_id": "5cc3b908-e619-4b99-88e5-2cf7f45965bd",
                    "smooth_streaming": False,
                    "target_origin_id": "frontend-erjan-result.s3.us-east-1.amazonaws.com",
                    "viewer_protocol_policy": "allow-all"
                },
                "comment": "RESULT",
                "price_class": "PriceClass_All",
                "enabled": True,
                "viewer_certificate": {
                    "cloud_front_default_certificate": True,
                    "minimum_protocol_version": "TLSv1",
                    "ssl_support_method": "vip"
                },
                "restrictions": {
                    "geo_restriction": {
                        "restriction_type": "none"
                    }
                },
                "http_version": "http2",
                "default_root_object": "index.html",
                "i_p_v6_enabled": True,
                "logging": {
                    "bucket": "cf-result-logs.s3.amazonaws.com",
                    "include_cookies": False,
                    "prefix": "who-viewed-when"
                }
            }
        )

        cloudfrontdistribution2 = cloudfront.CfnDistribution(
            self,
            "CloudFrontDistribution2",
            distribution_config={
                "origins": [
                    {
                        "connection_attempts": 3,
                        "connection_timeout": 10,
                        "domain_name": "frontend-erjan-vote.s3.us-east-1.amazonaws.com",
                        "id": "frontend-erjan-vote.s3.us-east-1.amazonaws.com",
                        "origin_path": "",
                        "s3_origin_config": {
                            "origin_access_identity": "origin-access-identity/cloudfront/E2NHXOJ7VCG7IJ"
                        }
                    }
                ],
                "default_cache_behavior": {
                    "allowed_methods": [
                        "HEAD",
                        "DELETE",
                        "POST",
                        "GET",
                        "OPTIONS",
                        "PUT",
                        "PATCH"
                    ],
                    "cached_methods": [
                        "HEAD",
                        "GET",
                        "OPTIONS"
                    ],
                    "compress": True,
                    "cache_policy_id": "658327ea-f89d-4fab-a63d-7e88639e58f6",
                    "origin_request_policy_id": "88a5eaf4-2fd4-4709-b370-b4c650ea3fcf",
                    "response_headers_policy_id": "5cc3b908-e619-4b99-88e5-2cf7f45965bd",
                    "smooth_streaming": False,
                    "target_origin_id": "frontend-erjan-vote.s3.us-east-1.amazonaws.com",
                    "viewer_protocol_policy": "allow-all"
                },
                "comment": "VOTE",
                "price_class": "PriceClass_All",
                "enabled": True,
                "viewer_certificate": {
                    "cloud_front_default_certificate": True,
                    "minimum_protocol_version": "TLSv1",
                    "ssl_support_method": "vip"
                },
                "restrictions": {
                    "geo_restriction": {
                        "restriction_type": "none"
                    }
                },
                "http_version": "http2",
                "default_root_object": "index.html",
                "i_p_v6_enabled": True,
                "logging": {
                    "bucket": "cf-vote-logs.s3.amazonaws.com",
                    "include_cookies": False,
                    "prefix": "who-voted-when"
                }
            }
        )

        ec2instance = ec2.CfnInstance(
            self,
            "EC2Instance",
            image_id="ami-0b5eea76982371e91",
            instance_type="t2.micro",
            key_name="myvote",
            availability_zone=ec2subnet.attr_availability_zone,
            tenancy="default",
            subnet_id=ec2subnet.ref,
            ebs_optimized=False,
            security_group_ids=[
                "sg-01afc2eba5b520f9b"
            ],
            source_dest_check=True,
            block_device_mappings=[
                {
                    "device_name": "/dev/xvda",
                    "ebs": {
                        "encrypted": False,
                        "volume_size": 8,
                        "snapshot_id": "snap-097c82c1f068b49cb",
                        "volume_type": "gp2",
                        "delete_on_termination": True
                    }
                }
            ],
            user_data="IyEvYmluL2Jhc2gKY3VybCBodHRwczovL3Jhdy5naXRodWJ1c2VyY29udGVudC5jb20vZXJqYW4vTXlWb3RlQVdTL21haW4vdm90ZS1wcm9jZXNzb3IvcHJvY2Vzc29yLnB5ID4gcHJvY2Vzc29yLnB5CmNobW9kICt4IHByb2Nlc3Nvci5weQp5dW0gLXkgaW5zdGFsbCBweXRob24tcGlwCnB5dGhvbiAtbSBwaXAgaW5zdGFsbCAtLXVzZXIgYm90bzMKLi9wcm9jZXNzb3IucHk=",
            iam_instance_profile=iamrole6.ref,
            tags=[
                {
                    "key": "Name",
                    "value": "vote-processor"
                }
            ],
            hibernation_options={
                "configured": False
            },
            enclave_options={
                "enabled": False
            }
        )

        lambdafunction = _lambda.CfnFunction(
            self,
            "LambdaFunction",
            description="",
            function_name="results",
            handler="lambda_function.lambda_handler",
            architectures=[
                "x86_64"
            ],
            code={
                "s3_bucket": "prod-04-2014-tasks",
                "s3_key": "/snapshots/025416187662/results-3a33a067-c711-4a7c-a9b1-7d215068f6c3",
                "s3_object_version": "QiqpeChc6_Gs552IAgD7aBZZwykjSVne"
            },
            memory_size=128,
            role=iamrole4.attr_arn,
            runtime="python3.9",
            timeout=3,
            tracing_config={
                "mode": "PassThrough"
            },
            ephemeral_storage={
                "size": 512
            }
        )

        lambdafunction2 = _lambda.CfnFunction(
            self,
            "LambdaFunction2",
            description="",
            function_name="voting",
            handler="lambda_function.lambda_handler",
            architectures=[
                "x86_64"
            ],
            code={
                "s3_bucket": "prod-04-2014-tasks",
                "s3_key": "/snapshots/025416187662/voting-f2684d7f-4abb-4265-add7-edf4860adb28",
                "s3_object_version": "ZmtZwWWuw5iTqOyFk6YakhAeTTowkj5E"
            },
            memory_size=128,
            role=iamrole8.attr_arn,
            runtime="python3.9",
            timeout=3,
            tracing_config={
                "mode": "PassThrough"
            },
            ephemeral_storage={
                "size": 512
            }
        )

        s3bucket = s3.CfnBucket(
            self,
            "S3Bucket",
            bucket_name="frontend-erjan-result",
            tags=[
                {
                    "key": "frontend-result",
                    "value": ""
                }
            ],
            website_configuration={
                "index_document": "index.html"
            }
        )

        s3bucket2 = s3.CfnBucket(
            self,
            "S3Bucket2",
            bucket_name="frontend-erjan-vote",
            tags=[
                {
                    "key": "frontend",
                    "value": ""
                }
            ],
            logging_configuration={
                "destination_bucket_name": "erjan-vote-s3-access-logs",
                "log_file_prefix": ""
            },
            website_configuration={
                "index_document": "index.html"
            }
        )

        dynamodbtable = dynamodb.CfnTable(
            self,
            "DynamoDBTable",
            attribute_definitions=[
                {
                    "attribute_name": "voter",
                    "attribute_type": "S"
                }
            ],
            billing_mode="PAY_PER_REQUEST",
            table_name="Votes",
            key_schema=[
                {
                    "attribute_name": "voter",
                    "key_type": "HASH"
                }
            ],
            stream_specification={
                "stream_view_type": "NEW_AND_OLD_IMAGES"
            }
        )

        ec2vpc = ec2.CfnVPC(
            self,
            "EC2VPC",
            cidr_block="10.0.0.0/24",
            enable_dns_support=True,
            enable_dns_hostnames=True,
            instance_tenancy="default"
        )

        apigatewayv2api = apigatewayv2.CfnApi(
            self,
            "ApiGatewayV2Api",
            api_key_selection_expression="$request.header.x-api-key",
            description="api for project my vote",
            protocol_type="HTTP",
            route_selection_expression="$request.method $request.path",
            cors_configuration={
                "allow_credentials": False,
                "allow_headers": [
                    "accept",
                    "content-type"
                ],
                "allow_methods": [
                    "POST",
                    "GET",
                    "OPTIONS"
                ],
                "allow_origins": [
                    "https://d1wktfnq0mcp3y.cloudfront.net",
                    "https://d3u9gxsy6062na.cloudfront.net"
                ],
                "max_age": 0
            },
            disable_execute_api_endpoint=False
        )

        apigatewayv2stage = apigatewayv2.CfnStage(
            self,
            "ApiGatewayV2Stage",
            stage_name="$default",
            stage_variables={
                
            },
            api_id=apigatewayv2api.ref,
            deployment_id="b18cmm",
            route_settings={
                
            },
            default_route_settings={
                "detailed_metrics_enabled": False
            },
            auto_deploy=True
        )

        apigatewayv2route = apigatewayv2.CfnRoute(
            self,
            "ApiGatewayV2Route",
            api_id=apigatewayv2api.ref,
            api_key_required=False,
            authorization_type="NONE",
            request_parameters={
                
            },
            route_key="POST /voting",
            target="integrations/0lqx8dd"
        )

        apigatewayv2route2 = apigatewayv2.CfnRoute(
            self,
            "ApiGatewayV2Route2",
            api_id=apigatewayv2api.ref,
            api_key_required=False,
            authorization_type="NONE",
            request_parameters={
                
            },
            route_key="GET /results",
            target="integrations/mp5prlm"
        )

        apigatewayv2integration = apigatewayv2.CfnIntegration(
            self,
            "ApiGatewayV2Integration",
            api_id=apigatewayv2api.ref,
            connection_type="INTERNET",
            integration_method="POST",
            integration_type="AWS_PROXY",
            integration_uri=lambdafunction2.attr_arn,
            timeout_in_millis=30000,
            payload_format_version="2.0"
        )

        apigatewayv2integration2 = apigatewayv2.CfnIntegration(
            self,
            "ApiGatewayV2Integration2",
            api_id=apigatewayv2api.ref,
            connection_type="INTERNET",
            integration_method="POST",
            integration_type="AWS_PROXY",
            integration_uri=lambdafunction.attr_arn,
            timeout_in_millis=30000,
            payload_format_version="2.0"
        )

        apigatewayv2integration3 = apigatewayv2.CfnIntegration(
            self,
            "ApiGatewayV2Integration3",
            api_id=apigatewayv2api.ref,
            connection_type="INTERNET",
            integration_method="POST",
            integration_type="AWS_PROXY",
            integration_uri="arn:aws:lambda:us-east-1:025416187662:function:myfirstlambda",
            timeout_in_millis=30000,
            payload_format_version="2.0"
        )

        snstopicpolicy = sns.CfnTopicPolicy(
            self,
            "SNSTopicPolicy",
            policy_document="{\"Version\":\"2008-10-17\",\"Id\":\"__default_policy_ID\",\"Statement\":[{\"Sid\":\"__default_statement_ID\",\"Effect\":\"Allow\",\"Principal\":{\"AWS\":\"*\"},\"Action\":[\"SNS:Publish\",\"SNS:RemovePermission\",\"SNS:SetTopicAttributes\",\"SNS:DeleteTopic\",\"SNS:ListSubscriptionsByTopic\",\"SNS:GetTopicAttributes\",\"SNS:AddPermission\",\"SNS:Subscribe\"],\"Resource\":\"arn:aws:sns:us-east-1:025416187662:erjan\",\"Condition\":{\"StringEquals\":{\"AWS:SourceOwner\":\"025416187662\"}}},{\"Sid\":\"__console_pub_0\",\"Effect\":\"Allow\",\"Principal\":{\"AWS\":\"*\"},\"Action\":\"SNS:Publish\",\"Resource\":\"arn:aws:sns:us-east-1:025416187662:erjan\"},{\"Sid\":\"__console_sub_0\",\"Effect\":\"Allow\",\"Principal\":{\"AWS\":\"*\"},\"Action\":\"SNS:Subscribe\",\"Resource\":\"arn:aws:sns:us-east-1:025416187662:erjan\"}]}",
            topics=[
                snstopic.ref
            ]
        )

        snstopic = sns.CfnTopic(
            self,
            "SNSTopic",
            display_name=sqsqueue.attr_queue_name,
            topic_name=sqsqueue.attr_queue_name
        )

        snssubscription = sns.CfnSubscription(
            self,
            "SNSSubscription",
            topic_arn=snstopic.ref,
            endpoint=sqsqueue.ref,
            protocol="sqs",
            raw_message_delivery="true",
            region="us-east-1"
        )

        sqsqueue = sqs.CfnQueue(
            self,
            "SQSQueue",
            delay_seconds="0",
            maximum_message_size="262144",
            message_retention_period="345600",
            receive_message_wait_time_seconds="0",
            visibility_timeout="30",
            queue_name="erjan"
        )

        sqsqueuepolicy = sqs.CfnQueuePolicy(
            self,
            "SQSQueuePolicy",
            policy_document="{\"Version\":\"2008-10-17\",\"Id\":\"__default_policy_ID\",\"Statement\":[{\"Sid\":\"__owner_statement\",\"Effect\":\"Allow\",\"Principal\":{\"AWS\":\"arn:aws:iam::025416187662:root\"},\"Action\":\"SQS:*\",\"Resource\":\"arn:aws:sqs:us-east-1:025416187662:erjan\"},{\"Sid\":\"topic-subscription-arn:aws:sns:us-east-1:025416187662:erjan\",\"Effect\":\"Allow\",\"Principal\":{\"AWS\":\"*\"},\"Action\":\"SQS:SendMessage\",\"Resource\":\"arn:aws:sqs:us-east-1:025416187662:erjan\",\"Condition\":{\"ArnLike\":{\"aws:SourceArn\":\"arn:aws:sns:us-east-1:025416187662:erjan\"}}}]}",
            queues=[
                "https://sqs.us-east-1.amazonaws.com/025416187662/erjan"
            ]
        )

        iamrole = iam.CfnRole(
            self,
            "IAMRole",
            path="/service-role/",
            role_name="for_api-role-qvqsvvxs",
            assume_role_policy_document="{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"lambda.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}",
            max_session_duration=3600,
            managed_policy_arns=[
                "arn:aws:iam::025416187662:policy/service-role/AWSLambdaBasicExecutionRole-27dc851a-5f74-4cc2-9e6e-794f817ad711"
            ]
        )

        iamrole2 = iam.CfnRole(
            self,
            "IAMRole2",
            path="/service-role/",
            role_name="results-role-9stwb69a",
            assume_role_policy_document="{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"lambda.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}",
            max_session_duration=3600,
            managed_policy_arns=[
                "arn:aws:iam::025416187662:policy/service-role/AWSLambdaBasicExecutionRole-ef86603b-1836-4eef-91cd-d1cb8be35673"
            ]
        )

        iamrole3 = iam.CfnRole(
            self,
            "IAMRole3",
            path="/",
            role_name="s3-erjan",
            assume_role_policy_document="{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"s3.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}",
            max_session_duration=3600,
            managed_policy_arns=[
                "arn:aws:iam::aws:policy/TranslateReadOnly",
                "arn:aws:iam::aws:policy/TranslateFullAccess"
            ],
            description="Allows S3 to call AWS services on your behalf."
        )

        iamrole4 = iam.CfnRole(
            self,
            "IAMRole4",
            path="/service-role/",
            role_name="results-role-cs7bdnlc",
            assume_role_policy_document="{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"lambda.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}",
            max_session_duration=3600,
            managed_policy_arns=[
                iammanagedpolicy10.ref,
                iammanagedpolicy3.ref,
                "arn:aws:iam::025416187662:policy/service-role/AWSLambdaVPCAccessExecutionRole-716e4420-886d-452b-a2b9-d916cd7edcde",
                "arn:aws:iam::aws:policy/AWSLambdaInvocation-DynamoDB",
                "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
            ]
        )

        iamrole5 = iam.CfnRole(
            self,
            "IAMRole5",
            path="/",
            role_name="sqs_apigateway_role",
            assume_role_policy_document="{\"Version\":\"2012-10-17\",\"Statement\":[{\"Sid\":\"\",\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"apigateway.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}",
            max_session_duration=3600,
            managed_policy_arns=[
                "arn:aws:iam::aws:policy/service-role/AmazonAPIGatewayPushToCloudWatchLogs",
                "arn:aws:iam::aws:policy/AmazonSQSFullAccess"
            ],
            description="Allows API Gateway to push logs to CloudWatch Logs."
        )

        iamrole6 = iam.CfnRole(
            self,
            "IAMRole6",
            path="/",
            role_name="vote-processor-ec2-role",
            assume_role_policy_document="{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"ec2.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}",
            max_session_duration=3600,
            managed_policy_arns=[
                iammanagedpolicy7.ref,
                iammanagedpolicy5.ref
            ],
            description="vote processor can receive from sqs and send messages to dynamodb"
        )

        iamrole7 = iam.CfnRole(
            self,
            "IAMRole7",
            path="/service-role/",
            role_name="vote_processor_ec2-role-6r4x3dcf",
            assume_role_policy_document="{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"lambda.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}",
            max_session_duration=3600,
            managed_policy_arns=[
                iammanagedpolicy7.ref,
                iammanagedpolicy5.ref,
                "arn:aws:iam::025416187662:policy/service-role/AWSLambdaBasicExecutionRole-6cc57b7a-0289-4b56-a380-d0731b195cf5"
            ]
        )

        iamrole8 = iam.CfnRole(
            self,
            "IAMRole8",
            path="/service-role/",
            role_name="voting-role-z6z0brhg",
            assume_role_policy_document="{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"lambda.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}",
            max_session_duration=3600,
            managed_policy_arns=[
                iammanagedpolicy6.ref,
                "arn:aws:iam::025416187662:policy/service-role/AWSLambdaVPCAccessExecutionRole-716e4420-886d-452b-a2b9-d916cd7edcde",
                "arn:aws:iam::025416187662:policy/service-role/AWSLambdaBasicExecutionRole-427c92eb-1f05-4b19-b56b-5a9a21c52886"
            ]
        )

        iamrole9 = iam.CfnRole(
            self,
            "IAMRole9",
            path="/service-role/",
            role_name="voting-role-tiym3gs8",
            assume_role_policy_document="{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"lambda.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}",
            max_session_duration=3600,
            managed_policy_arns=[
                iammanagedpolicy2.ref,
                "arn:aws:iam::025416187662:policy/service-role/AWSLambdaSNSTopicDestinationExecutionRole-b1f9acb5-8c51-4416-9acd-2a62c7d445fc",
                iammanagedpolicy4.ref
            ]
        )

        iamservicelinkedrole = iam.CfnServiceLinkedRole(
            self,
            "IAMServiceLinkedRole",
            a_w_s_service_name="ops.apigateway.amazonaws.com",
            description="The Service Linked Role is used by Amazon API Gateway."
        )

        iammanagedpolicy = iam.CfnManagedPolicy(
            self,
            "IAMManagedPolicy",
            managed_policy_name="AWSLambdaBasicExecutionRole-26905855-e012-4435-a907-3405124b0309",
            path="/service-role/",
            policy_document='''
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "logs:CreateLogGroup",
            "Resource": "arn:aws:logs:us-east-1:025416187662:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": [
                "arn:aws:logs:us-east-1:025416187662:log-group:/aws/lambda/resize-image-kenjegalee:*"
            ]
        }
    ]
}
'''
        )

        iammanagedpolicy2 = iam.CfnManagedPolicy(
            self,
            "IAMManagedPolicy2",
            managed_policy_name="AWSLambdaBasicExecutionRole-b4e0f21f-4840-4bfa-b6e1-e0f9b62c73c7",
            path="/service-role/",
            policy_document='''
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "logs:CreateLogGroup",
            "Resource": "arn:aws:logs:us-east-1:025416187662:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": [
                "arn:aws:logs:us-east-1:025416187662:log-group:/aws/lambda/voting:*"
            ]
        }
    ]
}
'''
        )

        iammanagedpolicy3 = iam.CfnManagedPolicy(
            self,
            "IAMManagedPolicy3",
            managed_policy_name="AWSLambdaBasicExecutionRole-dbca2dcf-f8e8-49d6-bb7c-5ff50e1c8cef",
            path="/service-role/",
            policy_document='''
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "logs:CreateLogGroup",
            "Resource": "arn:aws:logs:us-east-1:025416187662:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": [
                "arn:aws:logs:us-east-1:025416187662:log-group:/aws/lambda/results:*"
            ]
        }
    ]
}
'''
        )

        iammanagedpolicy4 = iam.CfnManagedPolicy(
            self,
            "IAMManagedPolicy4",
            managed_policy_name="AWSLambdaVPCAccessExecutionRole-3a7912c6-f863-4299-b9d1-3a29dd14736e",
            path="/service-role/",
            policy_document='''
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:CreateNetworkInterface",
                "ec2:DeleteNetworkInterface",
                "ec2:DescribeNetworkInterfaces"
            ],
            "Resource": "*"
        }
    ]
}
'''
        )

        iammanagedpolicy5 = iam.CfnManagedPolicy(
            self,
            "IAMManagedPolicy5",
            managed_policy_name="ec2-can-access-sqs",
            path="/",
            policy_document='''
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "sqs:DeleteMessage",
                "sqs:GetQueueUrl",
                "sqs:ReceiveMessage"
            ],
            "Resource": "arn:aws:sqs:us-east-1:025416187662:erjan"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": "sqs:GetQueueAttributes",
            "Resource": "arn:aws:sqs:us-east-1:025416187662:erjan"
        }
    ]
}
'''
        )

        iammanagedpolicy6 = iam.CfnManagedPolicy(
            self,
            "IAMManagedPolicy6",
            managed_policy_name="voting-backend-can-send-to-sns",
            path="/",
            policy_document='''
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "sns:Publish"
            ],
            "Resource": "arn:aws:sns:us-east-1:025416187662:erjan"
        }
    ]
}
'''
        )

        iammanagedpolicy7 = iam.CfnManagedPolicy(
            self,
            "IAMManagedPolicy7",
            managed_policy_name="ec2-can-access-dynamodb",
            path="/",
            policy_document='''
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "dynamodb:PutItem",
                "dynamodb:UpdateItem",
                "dynamodb:Get*",
                "dynamodb:Query",
                "dynamodb:Scan",
                "dynamodb:BatchWrite*",
                "dynamodb:CreateTable",
                "dynamodb:Delete*"
                
            ],
            "Resource": "arn:aws:dynamodb:us-east-1:025416187662:table/Votes"
        }
    ]
}
'''
        )

        iammanagedpolicy8 = iam.CfnManagedPolicy(
            self,
            "IAMManagedPolicy8",
            managed_policy_name="dynamodb_access_votes",
            path="/",
            policy_document='''
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:PutItem",
                "dynamodb:UpdateItem"
            ],
            "Resource": "arn:aws:dynamodb:us-east-1:025416187662:table/Votes"
        }
    ]
}
'''
        )

        iammanagedpolicy9 = iam.CfnManagedPolicy(
            self,
            "IAMManagedPolicy9",
            managed_policy_name="votes-test-dynamodb-lambda-get-item-policy",
            path="/",
            policy_document='''
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
            "Resource": "arn:aws:dynamodb:us-east-1:025416187662:table/votes-test"
        }
    ]
}
'''
        )

        iammanagedpolicy10 = iam.CfnManagedPolicy(
            self,
            "IAMManagedPolicy10",
            managed_policy_name="lambda_invoke_dynamodb_get_item",
            path="/",
            policy_document='''
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
'''
        )

        iammanagedpolicy11 = iam.CfnManagedPolicy(
            self,
            "IAMManagedPolicy11",
            managed_policy_name="sqs-erjan-my-vote",
            path="/",
            policy_document='''
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
            "Resource": "arn:aws:sqs:us-east-1:025416187662:erjan"
        }
    ]
}
'''
        )

        iaminstanceprofile = iam.CfnInstanceProfile(
            self,
            "IAMInstanceProfile",
            path="/",
            instance_profile_name=iamrole6.ref,
            roles=[
                iamrole6.ref
            ]
        )

        iamaccesskey = iam.CfnAccessKey(
            self,
            "IAMAccessKey",
            status="Active",
            user_name="admin"
        )

        iamaccesskey2 = iam.CfnAccessKey(
            self,
            "IAMAccessKey2",
            status="Active",
            user_name="former2-iac-generator"
        )

        ec2volume = ec2.CfnVolume(
            self,
            "EC2Volume",
            availability_zone=ec2instance.attr_availability_zone,
            encrypted=False,
            size=8,
            volume_type="gp2",
            snapshot_id="snap-097c82c1f068b49cb",
            multi_attach_enabled=False
        )

        ec2networkinterface = ec2.CfnNetworkInterface(
            self,
            "EC2NetworkInterface",
            description="AWS Lambda VPC ENI-voting-434f3861-dec2-41e2-8871-aba9fbb9d218",
            private_ip_address="10.0.0.45",
            private_ip_addresses=[
                {
                    "private_ip_address": "10.0.0.45",
                    "primary": True
                }
            ],
            subnet_id=ec2subnet.ref,
            source_dest_check=True,
            group_set=[
                "sg-01afc2eba5b520f9b"
            ]
        )

        ec2networkinterface2 = ec2.CfnNetworkInterface(
            self,
            "EC2NetworkInterface2",
            description="",
            private_ip_address=ec2instance.attr_private_ip,
            private_ip_addresses=[
                {
                    "private_ip_address": ec2instance.attr_private_ip,
                    "primary": True
                }
            ],
            subnet_id=ec2subnet.ref,
            source_dest_check=True,
            group_set=[
                "sg-01afc2eba5b520f9b"
            ]
        )

        ec2networkinterfaceattachment = ec2.CfnNetworkInterfaceAttachment(
            self,
            "EC2NetworkInterfaceAttachment",
            network_interface_id="eni-04c7a8adb7484ca50",
            device_index=0,
            instance_id=ec2instance.ref,
            delete_on_termination=True
        )

        ec2vpccidrblock = ec2.CfnVPCCidrBlock(
            self,
            "EC2VPCCidrBlock",
            vpc_id=ec2vpc.ref,
            ipv6_cidr_block="2600:1f10:4453:6100::/56",
            ipv6_pool="Amazon"
        )

        ec2subnet = ec2.CfnSubnet(
            self,
            "EC2Subnet",
            availability_zone="us-east-1d",
            cidr_block=ec2vpc.attr_cidr_block,
            vpc_id=ec2vpc.ref,
            map_public_ip_on_launch=False,
            tags=[
                {
                    "key": "Name",
                    "value": "subnet1"
                }
            ]
        )

        ec2internetgateway = ec2.CfnInternetGateway(
            self,
            "EC2InternetGateway",
            tags=[
                {
                    "key": "Name",
                    "value": "ll"
                }
            ]
        )

        ec2eip = ec2.CfnEIP(
            self,
            "EC2EIP",
            domain="vpc"
        )

        ec2route = ec2.CfnRoute(
            self,
            "EC2Route",
            destination_cidr_block="0.0.0.0/0",
            gateway_id=ec2internetgateway.ref,
            route_table_id=ec2routetable.ref
        )

        ec2routetable = ec2.CfnRouteTable(
            self,
            "EC2RouteTable",
            vpc_id=ec2vpc.ref
        )


app = cdk.App()
MyStack(app, "my-stack-name", env={'region': 'us-east-1'})
app.synth()