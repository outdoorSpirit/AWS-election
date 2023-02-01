terraform {
    required_providers {
        aws = {
            source = "hashicorp/aws"
            version = "~> 3.0"
        }
    }
}

provider "aws" {
    region = "us-east-1"
}

resource "aws_cloudfront_distribution" "CloudFrontDistribution" {
    origin {
        domain_name = "frontend-erjan-result.s3.us-east-1.amazonaws.com"
        origin_id = "frontend-erjan-result.s3.us-east-1.amazonaws.com"
        
        origin_path = ""
        s3_origin_config {
            origin_access_identity = "origin-access-identity/cloudfront/E36TPZ2E5JVKVL"
        }
    }
    default_cache_behavior {
        allowed_methods = [
            "HEAD",
            "GET",
            "OPTIONS"
        ]
        compress = true
        smooth_streaming  = false
        target_origin_id = "frontend-erjan-result.s3.us-east-1.amazonaws.com"
        viewer_protocol_policy = "allow-all"
    }
    comment = "RESULT"
    price_class = "PriceClass_All"
    enabled = true
    viewer_certificate {
        cloudfront_default_certificate = true
        minimum_protocol_version = "TLSv1"
        ssl_support_method = "vip"
    }
    restrictions {
        geo_restriction {
            restriction_type = "none"
        }
    }
    http_version = "http2"
    is_ipv6_enabled = true
}

resource "aws_cloudfront_distribution" "CloudFrontDistribution2" {
    origin {
        domain_name = "frontend-erjan-vote.s3.us-east-1.amazonaws.com"
        origin_id = "frontend-erjan-vote.s3.us-east-1.amazonaws.com"
        
        origin_path = ""
        s3_origin_config {
            origin_access_identity = "origin-access-identity/cloudfront/E2NHXOJ7VCG7IJ"
        }
    }
    default_cache_behavior {
        allowed_methods = [
            "HEAD",
            "DELETE",
            "POST",
            "GET",
            "OPTIONS",
            "PUT",
            "PATCH"
        ]
        compress = true
        smooth_streaming  = false
        target_origin_id = "frontend-erjan-vote.s3.us-east-1.amazonaws.com"
        viewer_protocol_policy = "allow-all"
    }
    comment = "VOTE"
    price_class = "PriceClass_All"
    enabled = true
    viewer_certificate {
        cloudfront_default_certificate = true
        minimum_protocol_version = "TLSv1"
        ssl_support_method = "vip"
    }
    restrictions {
        geo_restriction {
            restriction_type = "none"
        }
    }
    http_version = "http2"
    is_ipv6_enabled = true
}

resource "aws_instance" "EC2Instance" {
    ami = "ami-0b5eea76982371e91"
    instance_type = "t2.micro"
    key_name = "myvote"
    availability_zone = "us-east-1d"
    tenancy = "default"
    subnet_id = "subnet-03c9ba79c131f780f"
    ebs_optimized = false
    vpc_security_group_ids = [
        "sg-01afc2eba5b520f9b"
    ]
    source_dest_check = true
    root_block_device {
        volume_size = 8
        volume_type = "gp2"
        delete_on_termination = true
    }
    user_data = "IyEvYmluL2Jhc2gKY3VybCBodHRwczovL3Jhdy5naXRodWJ1c2VyY29udGVudC5jb20vZXJqYW4vTXlWb3RlQVdTL21haW4vdm90ZS1wcm9jZXNzb3IvcHJvY2Vzc29yLnB5ID4gcHJvY2Vzc29yLnB5CmNobW9kICt4IHByb2Nlc3Nvci5weQp5dW0gLXkgaW5zdGFsbCBweXRob24tcGlwCnB5dGhvbiAtbSBwaXAgaW5zdGFsbCAtLXVzZXIgYm90bzMKLi9wcm9jZXNzb3IucHk="
    iam_instance_profile = "${aws_iam_role.IAMRole6.name}"
    tags = 
}

resource "aws_lambda_function" "LambdaFunction" {
    description = ""
    function_name = "results"
    handler = "lambda_function.lambda_handler"
    architectures = [
        "x86_64"
    ]
    s3_bucket = "prod-04-2014-tasks"
    s3_key = "/snapshots/025416187662/results-3a33a067-c711-4a7c-a9b1-7d215068f6c3"
    s3_object_version = "QiqpeChc6_Gs552IAgD7aBZZwykjSVne"
    memory_size = 128
    role = "${aws_iam_role.IAMRole4.arn}"
    runtime = "python3.9"
    timeout = 3
    tracing_config {
        mode = "PassThrough"
    }
}

resource "aws_lambda_function" "LambdaFunction2" {
    description = ""
    function_name = "voting"
    handler = "lambda_function.lambda_handler"
    architectures = [
        "x86_64"
    ]
    s3_bucket = "prod-04-2014-tasks"
    s3_key = "/snapshots/025416187662/voting-f2684d7f-4abb-4265-add7-edf4860adb28"
    s3_object_version = "ZmtZwWWuw5iTqOyFk6YakhAeTTowkj5E"
    memory_size = 128
    role = "${aws_iam_role.IAMRole8.arn}"
    runtime = "python3.9"
    timeout = 3
    tracing_config {
        mode = "PassThrough"
    }
}

resource "aws_s3_bucket" "S3Bucket" {
    bucket = "frontend-erjan-result"
}

resource "aws_s3_bucket" "S3Bucket2" {
    bucket = "frontend-erjan-vote"
}

resource "aws_dynamodb_table" "DynamoDBTable" {
    attribute {
        name = "voter"
        type = "S"
    }
    billing_mode = "PAY_PER_REQUEST"
    name = "Votes"
    hash_key = "voter"
    stream_enabled = true
    stream_view_type = "NEW_AND_OLD_IMAGES"
}

resource "aws_vpc" "EC2VPC" {
    cidr_block = "10.0.0.0/24"
    enable_dns_support = true
    enable_dns_hostnames = true
    instance_tenancy = "default"
    tags = 
}

resource "aws_apigatewayv2_api" "ApiGatewayV2Api" {
    api_key_selection_expression = "$request.header.x-api-key"
    description = "api for project my vote"
    protocol_type = "HTTP"
    route_selection_expression = "$request.method $request.path"
    cors_configuration {
        allow_credentials = false
        allow_headers = [
            "accept",
            "content-type"
        ]
        allow_methods = [
            "POST",
            "GET",
            "OPTIONS"
        ]
        allow_origins = [
            "https://d1wktfnq0mcp3y.cloudfront.net",
            "https://d3u9gxsy6062na.cloudfront.net"
        ]
        max_age = 0
    }
    tags = 
}

resource "aws_apigatewayv2_stage" "ApiGatewayV2Stage" {
    name = "$default"
    stage_variables {}
    api_id = "${aws_apigatewayv2_api.ApiGatewayV2Api.id}"
    deployment_id = "b18cmm"
    default_route_settings {
        detailed_metrics_enabled = false
    }
    auto_deploy = true
    tags = 
}

resource "aws_apigatewayv2_route" "ApiGatewayV2Route" {
    api_id = "${aws_apigatewayv2_api.ApiGatewayV2Api.id}"
    api_key_required = false
    authorization_type = "NONE"
    route_key = "POST /voting"
    target = "integrations/0lqx8dd"
}

resource "aws_apigatewayv2_route" "ApiGatewayV2Route2" {
    api_id = "${aws_apigatewayv2_api.ApiGatewayV2Api.id}"
    api_key_required = false
    authorization_type = "NONE"
    route_key = "GET /results"
    target = "integrations/mp5prlm"
}

resource "aws_apigatewayv2_integration" "ApiGatewayV2Integration" {
    api_id = "${aws_apigatewayv2_api.ApiGatewayV2Api.id}"
    connection_type = "INTERNET"
    integration_method = "POST"
    integration_type = "AWS_PROXY"
    integration_uri = "${aws_lambda_function.LambdaFunction2.arn}"
    timeout_milliseconds = 30000
    payload_format_version = "2.0"
}

resource "aws_apigatewayv2_integration" "ApiGatewayV2Integration2" {
    api_id = "${aws_apigatewayv2_api.ApiGatewayV2Api.id}"
    connection_type = "INTERNET"
    integration_method = "POST"
    integration_type = "AWS_PROXY"
    integration_uri = "${aws_lambda_function.LambdaFunction.arn}"
    timeout_milliseconds = 30000
    payload_format_version = "2.0"
}

resource "aws_apigatewayv2_integration" "ApiGatewayV2Integration3" {
    api_id = "${aws_apigatewayv2_api.ApiGatewayV2Api.id}"
    connection_type = "INTERNET"
    integration_method = "POST"
    integration_type = "AWS_PROXY"
    integration_uri = "arn:aws:lambda:us-east-1:025416187662:function:myfirstlambda"
    timeout_milliseconds = 30000
    payload_format_version = "2.0"
}

resource "aws_sns_topic_policy" "SNSTopicPolicy" {
    policy = "{\"Version\":\"2008-10-17\",\"Id\":\"__default_policy_ID\",\"Statement\":[{\"Sid\":\"__default_statement_ID\",\"Effect\":\"Allow\",\"Principal\":{\"AWS\":\"*\"},\"Action\":[\"SNS:Publish\",\"SNS:RemovePermission\",\"SNS:SetTopicAttributes\",\"SNS:DeleteTopic\",\"SNS:ListSubscriptionsByTopic\",\"SNS:GetTopicAttributes\",\"SNS:AddPermission\",\"SNS:Subscribe\"],\"Resource\":\"arn:aws:sns:us-east-1:025416187662:erjan\",\"Condition\":{\"StringEquals\":{\"AWS:SourceOwner\":\"025416187662\"}}},{\"Sid\":\"__console_pub_0\",\"Effect\":\"Allow\",\"Principal\":{\"AWS\":\"*\"},\"Action\":\"SNS:Publish\",\"Resource\":\"arn:aws:sns:us-east-1:025416187662:erjan\"},{\"Sid\":\"__console_sub_0\",\"Effect\":\"Allow\",\"Principal\":{\"AWS\":\"*\"},\"Action\":\"SNS:Subscribe\",\"Resource\":\"arn:aws:sns:us-east-1:025416187662:erjan\"}]}"
    arn = "arn:aws:sns:us-east-1:025416187662:erjan"
}

resource "aws_sns_topic" "SNSTopic" {
    display_name = "erjan"
    name = "erjan"
}

resource "aws_sns_topic_subscription" "SNSSubscription" {
    topic_arn = "arn:aws:sns:us-east-1:025416187662:erjan"
    endpoint = "arn:aws:sqs:us-east-1:025416187662:erjan"
    protocol = "sqs"
    raw_message_delivery = "true"
}

resource "aws_sqs_queue" "SQSQueue" {
    delay_seconds = "0"
    max_message_size = "262144"
    message_retention_seconds = "345600"
    receive_wait_time_seconds = "0"
    visibility_timeout_seconds = "30"
    name = "erjan"
}

resource "aws_sqs_queue_policy" "SQSQueuePolicy" {
    policy = "{\"Version\":\"2008-10-17\",\"Id\":\"__default_policy_ID\",\"Statement\":[{\"Sid\":\"__owner_statement\",\"Effect\":\"Allow\",\"Principal\":{\"AWS\":\"arn:aws:iam::025416187662:root\"},\"Action\":\"SQS:*\",\"Resource\":\"arn:aws:sqs:us-east-1:025416187662:erjan\"},{\"Sid\":\"topic-subscription-arn:aws:sns:us-east-1:025416187662:erjan\",\"Effect\":\"Allow\",\"Principal\":{\"AWS\":\"*\"},\"Action\":\"SQS:SendMessage\",\"Resource\":\"arn:aws:sqs:us-east-1:025416187662:erjan\",\"Condition\":{\"ArnLike\":{\"aws:SourceArn\":\"arn:aws:sns:us-east-1:025416187662:erjan\"}}}]}"
    queue_url = "https://sqs.us-east-1.amazonaws.com/025416187662/erjan"
}

resource "aws_iam_role" "IAMRole" {
    path = "/service-role/"
    name = "for_api-role-qvqsvvxs"
    assume_role_policy = "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"lambda.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}"
    max_session_duration = 3600
    tags = 
}

resource "aws_iam_role" "IAMRole2" {
    path = "/service-role/"
    name = "results-role-9stwb69a"
    assume_role_policy = "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"lambda.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}"
    max_session_duration = 3600
    tags = 
}

resource "aws_iam_role" "IAMRole3" {
    path = "/"
    name = "s3-erjan"
    assume_role_policy = "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"s3.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}"
    max_session_duration = 3600
    tags = 
}

resource "aws_iam_role" "IAMRole4" {
    path = "/service-role/"
    name = "results-role-cs7bdnlc"
    assume_role_policy = "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"lambda.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}"
    max_session_duration = 3600
    tags = 
}

resource "aws_iam_role" "IAMRole5" {
    path = "/"
    name = "sqs_apigateway_role"
    assume_role_policy = "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Sid\":\"\",\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"apigateway.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}"
    max_session_duration = 3600
    tags = 
}

resource "aws_iam_role" "IAMRole6" {
    path = "/"
    name = "vote-processor-ec2-role"
    assume_role_policy = "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"ec2.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}"
    max_session_duration = 3600
    tags = 
}

resource "aws_iam_role" "IAMRole7" {
    path = "/service-role/"
    name = "vote_processor_ec2-role-6r4x3dcf"
    assume_role_policy = "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"lambda.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}"
    max_session_duration = 3600
    tags = 
}

resource "aws_iam_role" "IAMRole8" {
    path = "/service-role/"
    name = "voting-role-z6z0brhg"
    assume_role_policy = "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"lambda.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}"
    max_session_duration = 3600
    tags = 
}

resource "aws_iam_role" "IAMRole9" {
    path = "/service-role/"
    name = "voting-role-tiym3gs8"
    assume_role_policy = "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"lambda.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}"
    max_session_duration = 3600
    tags = 
}

resource "aws_iam_service_linked_role" "IAMServiceLinkedRole" {
    aws_service_name = "ops.apigateway.amazonaws.com"
    description = "The Service Linked Role is used by Amazon API Gateway."
}

resource "aws_iam_policy" "IAMManagedPolicy" {
    name = "AWSLambdaBasicExecutionRole-26905855-e012-4435-a907-3405124b0309"
    path = "/service-role/"
    policy = <<EOF
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
EOF
}

resource "aws_iam_policy" "IAMManagedPolicy2" {
    name = "AWSLambdaBasicExecutionRole-b4e0f21f-4840-4bfa-b6e1-e0f9b62c73c7"
    path = "/service-role/"
    policy = <<EOF
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
EOF
}

resource "aws_iam_policy" "IAMManagedPolicy3" {
    name = "AWSLambdaBasicExecutionRole-dbca2dcf-f8e8-49d6-bb7c-5ff50e1c8cef"
    path = "/service-role/"
    policy = <<EOF
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
EOF
}

resource "aws_iam_policy" "IAMManagedPolicy4" {
    name = "AWSLambdaVPCAccessExecutionRole-3a7912c6-f863-4299-b9d1-3a29dd14736e"
    path = "/service-role/"
    policy = <<EOF
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
EOF
}

resource "aws_iam_policy" "IAMManagedPolicy5" {
    name = "ec2-can-access-sqs"
    path = "/"
    policy = <<EOF
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
EOF
}

resource "aws_iam_policy" "IAMManagedPolicy6" {
    name = "voting-backend-can-send-to-sns"
    path = "/"
    policy = <<EOF
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
EOF
}

resource "aws_iam_policy" "IAMManagedPolicy7" {
    name = "ec2-can-access-dynamodb"
    path = "/"
    policy = <<EOF
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
EOF
}

resource "aws_iam_policy" "IAMManagedPolicy8" {
    name = "dynamodb_access_votes"
    path = "/"
    policy = <<EOF
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
EOF
}

resource "aws_iam_policy" "IAMManagedPolicy9" {
    name = "votes-test-dynamodb-lambda-get-item-policy"
    path = "/"
    policy = <<EOF
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
EOF
}

resource "aws_iam_policy" "IAMManagedPolicy10" {
    name = "lambda_invoke_dynamodb_get_item"
    path = "/"
    policy = <<EOF
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
EOF
}

resource "aws_iam_policy" "IAMManagedPolicy11" {
    name = "sqs-erjan-my-vote"
    path = "/"
    policy = <<EOF
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
EOF
}

resource "aws_iam_instance_profile" "IAMInstanceProfile" {
    path = "/"
    name = "${aws_iam_role.IAMRole6.name}"
    roles = [
        "${aws_iam_role.IAMRole6.name}"
    ]
}

resource "aws_iam_access_key" "IAMAccessKey" {
    status = "Active"
    user = "admin"
}

resource "aws_iam_access_key" "IAMAccessKey2" {
    status = "Active"
    user = "former2-iac-generator"
}

resource "aws_ebs_volume" "EC2Volume" {
    availability_zone = "us-east-1d"
    encrypted = false
    size = 8
    type = "gp2"
    snapshot_id = "snap-097c82c1f068b49cb"
    tags = 
}

resource "aws_network_interface" "EC2NetworkInterface" {
    description = "AWS Lambda VPC ENI-voting-434f3861-dec2-41e2-8871-aba9fbb9d218"
    private_ips = [
        "10.0.0.45"
    ]
    subnet_id = "subnet-03c9ba79c131f780f"
    source_dest_check = true
    security_groups = [
        "sg-01afc2eba5b520f9b"
    ]
}

resource "aws_network_interface" "EC2NetworkInterface2" {
    description = ""
    private_ips = [
        "10.0.0.129"
    ]
    subnet_id = "subnet-03c9ba79c131f780f"
    source_dest_check = true
    security_groups = [
        "sg-01afc2eba5b520f9b"
    ]
}

resource "aws_network_interface_attachment" "EC2NetworkInterfaceAttachment" {
    network_interface_id = "eni-04c7a8adb7484ca50"
    device_index = 0
    instance_id = "i-057a9d40a9e5a41ff"
}

resource "aws_vpc_ipv4_cidr_block_association" "EC2VPCCidrBlock" {
    vpc_id = "${aws_vpc.EC2VPC.id}"
}

resource "aws_subnet" "EC2Subnet" {
    availability_zone = "us-east-1d"
    cidr_block = "${aws_vpc.EC2VPC.cidr_block}"
    vpc_id = "${aws_vpc.EC2VPC.id}"
    map_public_ip_on_launch = false
}

resource "aws_internet_gateway" "EC2InternetGateway" {
    tags = 
    vpc_id = "${aws_vpc.EC2VPC.id}"
}

resource "aws_eip" "EC2EIP" {
    vpc = true
}

resource "aws_route" "EC2Route" {
    destination_cidr_block = "0.0.0.0/0"
    gateway_id = "igw-067c712c04da342ee"
    route_table_id = "rtb-0b098a78a3e0406ef"
}

resource "aws_route_table" "EC2RouteTable" {
    vpc_id = "${aws_vpc.EC2VPC.id}"
    tags = 
}