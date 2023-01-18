from troposphere import cloudfront, ec2, awslambda, s3, dynamodb, apigatewayv2, sns, sqs, iam
from troposphere import Ref, GetAtt, Template

template = Template()

template.add_version("2010-09-09")

CloudFrontDistribution = template.add_resource(cloudfront.Distribution(
    'CloudFrontDistribution',
    DistributionConfig=cloudfront.DistributionConfig(
        Origins=[
            {
                "ConnectionAttempts": 3,
                "ConnectionTimeout": 10,
                "DomainName": "frontend-erjan-result.s3.us-east-1.amazonaws.com",
                "Id": "frontend-erjan-result.s3.us-east-1.amazonaws.com",
                "OriginPath": "",
                "S3OriginConfig": {
                    'OriginAccessIdentity': "origin-access-identity/cloudfront/E36TPZ2E5JVKVL"
                }
            }
        ],
        DefaultCacheBehavior=cloudfront.LambdaFunctionAssociation(
            AllowedMethods=[
                "HEAD",
                "GET",
                "OPTIONS"
            ],
            CachedMethods=[
                "HEAD",
                "GET",
                "OPTIONS"
            ],
            Compress=True,
            CachePolicyId="658327ea-f89d-4fab-a63d-7e88639e58f6",
            OriginRequestPolicyId="88a5eaf4-2fd4-4709-b370-b4c650ea3fcf",
            ResponseHeadersPolicyId="5cc3b908-e619-4b99-88e5-2cf7f45965bd",
            SmoothStreaming=False,
            TargetOriginId="frontend-erjan-result.s3.us-east-1.amazonaws.com",
            ViewerProtocolPolicy="allow-all"
        ),
        Comment="RESULT",
        PriceClass="PriceClass_All",
        Enabled=True,
        ViewerCertificate=cloudfront.ViewerCertificate(
            CloudFrontDefaultCertificate=True,
            MinimumProtocolVersion="TLSv1",
            SslSupportMethod="vip"
        ),
        Restrictions=cloudfront.Restrictions(
            GeoRestriction=cloudfront.GeoRestriction(
                RestrictionType="none"
            )
        ),
        HttpVersion="http2",
        DefaultRootObject="index.html",
        IPV6Enabled=True,
        Logging=cloudfront.Logging(
            Bucket="cf-result-logs.s3.amazonaws.com",
            IncludeCookies=False,
            Prefix="who-viewed-when"
        )
    )
))

CloudFrontDistribution2 = template.add_resource(cloudfront.Distribution(
    'CloudFrontDistribution2',
    DistributionConfig=cloudfront.DistributionConfig(
        Origins=[
            {
                "ConnectionAttempts": 3,
                "ConnectionTimeout": 10,
                "DomainName": "frontend-erjan-vote.s3.us-east-1.amazonaws.com",
                "Id": "frontend-erjan-vote.s3.us-east-1.amazonaws.com",
                "OriginPath": "",
                "S3OriginConfig": {
                    'OriginAccessIdentity': "origin-access-identity/cloudfront/E2NHXOJ7VCG7IJ"
                }
            }
        ],
        DefaultCacheBehavior=cloudfront.LambdaFunctionAssociation(
            AllowedMethods=[
                "HEAD",
                "DELETE",
                "POST",
                "GET",
                "OPTIONS",
                "PUT",
                "PATCH"
            ],
            CachedMethods=[
                "HEAD",
                "GET",
                "OPTIONS"
            ],
            Compress=True,
            CachePolicyId="658327ea-f89d-4fab-a63d-7e88639e58f6",
            OriginRequestPolicyId="88a5eaf4-2fd4-4709-b370-b4c650ea3fcf",
            ResponseHeadersPolicyId="5cc3b908-e619-4b99-88e5-2cf7f45965bd",
            SmoothStreaming=False,
            TargetOriginId="frontend-erjan-vote.s3.us-east-1.amazonaws.com",
            ViewerProtocolPolicy="allow-all"
        ),
        Comment="VOTE",
        PriceClass="PriceClass_All",
        Enabled=True,
        ViewerCertificate=cloudfront.ViewerCertificate(
            CloudFrontDefaultCertificate=True,
            MinimumProtocolVersion="TLSv1",
            SslSupportMethod="vip"
        ),
        Restrictions=cloudfront.Restrictions(
            GeoRestriction=cloudfront.GeoRestriction(
                RestrictionType="none"
            )
        ),
        HttpVersion="http2",
        DefaultRootObject="index.html",
        IPV6Enabled=True,
        Logging=cloudfront.Logging(
            Bucket="cf-vote-logs.s3.amazonaws.com",
            IncludeCookies=False,
            Prefix="who-voted-when"
        )
    )
))

EC2Instance = template.add_resource(ec2.Instance(
    'EC2Instance',
    ImageId="ami-0b5eea76982371e91",
    InstanceType="t2.micro",
    KeyName="myvote",
    AvailabilityZone=GetAtt(EC2Subnet, 'AvailabilityZone'),
    Tenancy="default",
    SubnetId=Ref(EC2Subnet),
    EbsOptimized=False,
    SecurityGroupIds=[
        "sg-01afc2eba5b520f9b"
    ],
    SourceDestCheck=True,
    BlockDeviceMappings=[
        ec2.BlockDeviceMapping(
            DeviceName="/dev/xvda",
            Ebs=ec2.EBSBlockDevice(
                Encrypted=False,
                VolumeSize=8,
                SnapshotId="snap-097c82c1f068b49cb",
                VolumeType="gp2",
                DeleteOnTermination=True
            )
        )
    ],
    UserData="IyEvYmluL2Jhc2gKY3VybCBodHRwczovL3Jhdy5naXRodWJ1c2VyY29udGVudC5jb20vZXJqYW4vTXlWb3RlQVdTL21haW4vdm90ZS1wcm9jZXNzb3IvcHJvY2Vzc29yLnB5ID4gcHJvY2Vzc29yLnB5CmNobW9kICt4IHByb2Nlc3Nvci5weQp5dW0gLXkgaW5zdGFsbCBweXRob24tcGlwCnB5dGhvbiAtbSBwaXAgaW5zdGFsbCAtLXVzZXIgYm90bzMKLi9wcm9jZXNzb3IucHk=",
    IamInstanceProfile=Ref(IAMRole6),
    Tags=[
        {
            "Key": "Name",
            "Value": "vote-processor"
        }
    ],
    HibernationOptions={
        "Configured": False
    },
    EnclaveOptions={
        "Enabled": False
    }
))

LambdaFunction = template.add_resource(awslambda.Function(
    'LambdaFunction',
    Description="",
    FunctionName="results",
    Handler="lambda_function.lambda_handler",
    Architectures=[
        "x86_64"
    ],
    Code=awslambda.Code(
        S3Bucket="prod-04-2014-tasks",
        S3Key="/snapshots/025416187662/results-3a33a067-c711-4a7c-a9b1-7d215068f6c3",
        S3ObjectVersion="QiqpeChc6_Gs552IAgD7aBZZwykjSVne"
    ),
    MemorySize=128,
    Role=GetAtt(IAMRole4, 'Arn'),
    Runtime="python3.9",
    Timeout=3,
    TracingConfig=awslambda.TracingConfig(
        Mode="PassThrough"
    ),
    EphemeralStorage={
        "Size": 512
    }
))

LambdaFunction2 = template.add_resource(awslambda.Function(
    'LambdaFunction2',
    Description="",
    FunctionName="voting",
    Handler="lambda_function.lambda_handler",
    Architectures=[
        "x86_64"
    ],
    Code=awslambda.Code(
        S3Bucket="prod-04-2014-tasks",
        S3Key="/snapshots/025416187662/voting-f2684d7f-4abb-4265-add7-edf4860adb28",
        S3ObjectVersion="ZmtZwWWuw5iTqOyFk6YakhAeTTowkj5E"
    ),
    MemorySize=128,
    Role=GetAtt(IAMRole8, 'Arn'),
    Runtime="python3.9",
    Timeout=3,
    TracingConfig=awslambda.TracingConfig(
        Mode="PassThrough"
    ),
    EphemeralStorage={
        "Size": 512
    }
))

S3Bucket = template.add_resource(s3.Bucket(
    'S3Bucket',
    BucketName="frontend-erjan-result",
    Tags=[
        {
            "Key": "frontend-result",
            "Value": ""
        }
    ],
    WebsiteConfiguration=s3.WebsiteConfiguration(
        IndexDocument="index.html"
    )
))

S3Bucket2 = template.add_resource(s3.Bucket(
    'S3Bucket2',
    BucketName="frontend-erjan-vote",
    Tags=[
        {
            "Key": "frontend",
            "Value": ""
        }
    ],
    LoggingConfiguration=s3.LoggingConfiguration(
        DestinationBucketName="erjan-vote-s3-access-logs",
        LogFilePrefix=""
    ),
    WebsiteConfiguration=s3.WebsiteConfiguration(
        IndexDocument="index.html"
    )
))

DynamoDBTable = template.add_resource(dynamodb.Table(
    'DynamoDBTable',
    AttributeDefinitions=[
        dynamodb.AttributeDefinition(
            AttributeName="voter",
            AttributeType="S"
        )
    ],
    BillingMode="PAY_PER_REQUEST",
    TableName="Votes",
    KeySchema=[
        dynamodb.KeySchema(
            AttributeName="voter",
            KeyType="HASH"
        )
    ],
    StreamSpecification=dynamodb.StreamSpecification(
        StreamViewType="NEW_AND_OLD_IMAGES"
    )
))

EC2VPC = template.add_resource(ec2.VPC(
    'EC2VPC',
    CidrBlock="10.0.0.0/24",
    EnableDnsSupport=True,
    EnableDnsHostnames=True,
    InstanceTenancy="default"
))

ApiGatewayV2Api = template.add_resource(apigatewayv2.Api(
    'ApiGatewayV2Api',
    ApiKeySelectionExpression="$request.header.x-api-key",
    Description="api for project my vote",
    ProtocolType="HTTP",
    RouteSelectionExpression="$request.method $request.path",
    CorsConfiguration={
        "AllowCredentials": False,
        "AllowHeaders": [
            "accept",
            "content-type"
        ],
        "AllowMethods": [
            "POST",
            "GET",
            "OPTIONS"
        ],
        "AllowOrigins": [
            "https://d1wktfnq0mcp3y.cloudfront.net",
            "https://d3u9gxsy6062na.cloudfront.net"
        ],
        "MaxAge": 0
    },
    DisableExecuteApiEndpoint=False
))

ApiGatewayV2Stage = template.add_resource(apigatewayv2.Stage(
    'ApiGatewayV2Stage',
    StageName="$default",
    StageVariables={
        
    },
    ApiId=Ref(ApiGatewayV2Api),
    DeploymentId="b18cmm",
    RouteSettings={
        
    },
    DefaultRouteSettings={
        "DetailedMetricsEnabled": False
    },
    AutoDeploy=True
))

ApiGatewayV2Route = template.add_resource(apigatewayv2.Route(
    'ApiGatewayV2Route',
    ApiId=Ref(ApiGatewayV2Api),
    ApiKeyRequired=False,
    AuthorizationType="NONE",
    RequestParameters={
        
    },
    RouteKey="POST /voting",
    Target="integrations/0lqx8dd"
))

ApiGatewayV2Route2 = template.add_resource(apigatewayv2.Route(
    'ApiGatewayV2Route2',
    ApiId=Ref(ApiGatewayV2Api),
    ApiKeyRequired=False,
    AuthorizationType="NONE",
    RequestParameters={
        
    },
    RouteKey="GET /results",
    Target="integrations/mp5prlm"
))

ApiGatewayV2Integration = template.add_resource(apigatewayv2.Integration(
    'ApiGatewayV2Integration',
    ApiId=Ref(ApiGatewayV2Api),
    ConnectionType="INTERNET",
    IntegrationMethod="POST",
    IntegrationType="AWS_PROXY",
    IntegrationUri=GetAtt(LambdaFunction2, 'Arn'),
    TimeoutInMillis=30000,
    PayloadFormatVersion="2.0"
))

ApiGatewayV2Integration2 = template.add_resource(apigatewayv2.Integration(
    'ApiGatewayV2Integration2',
    ApiId=Ref(ApiGatewayV2Api),
    ConnectionType="INTERNET",
    IntegrationMethod="POST",
    IntegrationType="AWS_PROXY",
    IntegrationUri=GetAtt(LambdaFunction, 'Arn'),
    TimeoutInMillis=30000,
    PayloadFormatVersion="2.0"
))

ApiGatewayV2Integration3 = template.add_resource(apigatewayv2.Integration(
    'ApiGatewayV2Integration3',
    ApiId=Ref(ApiGatewayV2Api),
    ConnectionType="INTERNET",
    IntegrationMethod="POST",
    IntegrationType="AWS_PROXY",
    IntegrationUri="arn:aws:lambda:us-east-1:025416187662:function:myfirstlambda",
    TimeoutInMillis=30000,
    PayloadFormatVersion="2.0"
))

SNSTopicPolicy = template.add_resource(sns.TopicPolicy(
    'SNSTopicPolicy',
    PolicyDocument="{\"Version\":\"2008-10-17\",\"Id\":\"__default_policy_ID\",\"Statement\":[{\"Sid\":\"__default_statement_ID\",\"Effect\":\"Allow\",\"Principal\":{\"AWS\":\"*\"},\"Action\":[\"SNS:Publish\",\"SNS:RemovePermission\",\"SNS:SetTopicAttributes\",\"SNS:DeleteTopic\",\"SNS:ListSubscriptionsByTopic\",\"SNS:GetTopicAttributes\",\"SNS:AddPermission\",\"SNS:Subscribe\"],\"Resource\":\"arn:aws:sns:us-east-1:025416187662:erjan\",\"Condition\":{\"StringEquals\":{\"AWS:SourceOwner\":\"025416187662\"}}},{\"Sid\":\"__console_pub_0\",\"Effect\":\"Allow\",\"Principal\":{\"AWS\":\"*\"},\"Action\":\"SNS:Publish\",\"Resource\":\"arn:aws:sns:us-east-1:025416187662:erjan\"},{\"Sid\":\"__console_sub_0\",\"Effect\":\"Allow\",\"Principal\":{\"AWS\":\"*\"},\"Action\":\"SNS:Subscribe\",\"Resource\":\"arn:aws:sns:us-east-1:025416187662:erjan\"}]}",
    Topics=[
        Ref(SNSTopic)
    ]
))

SNSTopic = template.add_resource(sns.Topic(
    'SNSTopic',
    DisplayName=GetAtt(SQSQueue, 'QueueName'),
    TopicName=GetAtt(SQSQueue, 'QueueName')
))

SNSSubscription = template.add_resource(sns.SubscriptionResource(
    'SNSSubscription',
    TopicArn=Ref(SNSTopic),
    Endpoint=Ref(SQSQueue),
    Protocol="sqs",
    RawMessageDelivery="true",
    Region="us-east-1"
))

SQSQueue = template.add_resource(sqs.Queue(
    'SQSQueue',
    DelaySeconds="0",
    MaximumMessageSize="262144",
    MessageRetentionPeriod="345600",
    ReceiveMessageWaitTimeSeconds="0",
    VisibilityTimeout="30",
    QueueName="erjan"
))

SQSQueuePolicy = template.add_resource(sqs.QueuePolicy(
    'SQSQueuePolicy',
    PolicyDocument="{\"Version\":\"2008-10-17\",\"Id\":\"__default_policy_ID\",\"Statement\":[{\"Sid\":\"__owner_statement\",\"Effect\":\"Allow\",\"Principal\":{\"AWS\":\"arn:aws:iam::025416187662:root\"},\"Action\":\"SQS:*\",\"Resource\":\"arn:aws:sqs:us-east-1:025416187662:erjan\"},{\"Sid\":\"topic-subscription-arn:aws:sns:us-east-1:025416187662:erjan\",\"Effect\":\"Allow\",\"Principal\":{\"AWS\":\"*\"},\"Action\":\"SQS:SendMessage\",\"Resource\":\"arn:aws:sqs:us-east-1:025416187662:erjan\",\"Condition\":{\"ArnLike\":{\"aws:SourceArn\":\"arn:aws:sns:us-east-1:025416187662:erjan\"}}}]}",
    Queues=[
        "https://sqs.us-east-1.amazonaws.com/025416187662/erjan"
    ]
))

IAMRole = template.add_resource(iam.Role(
    'IAMRole',
    Path="/service-role/",
    RoleName="for_api-role-qvqsvvxs",
    AssumeRolePolicyDocument="{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"lambda.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}",
    MaxSessionDuration=3600,
    ManagedPolicyArns=[
        "arn:aws:iam::025416187662:policy/service-role/AWSLambdaBasicExecutionRole-27dc851a-5f74-4cc2-9e6e-794f817ad711"
    ]
))

IAMRole2 = template.add_resource(iam.Role(
    'IAMRole2',
    Path="/service-role/",
    RoleName="results-role-9stwb69a",
    AssumeRolePolicyDocument="{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"lambda.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}",
    MaxSessionDuration=3600,
    ManagedPolicyArns=[
        "arn:aws:iam::025416187662:policy/service-role/AWSLambdaBasicExecutionRole-ef86603b-1836-4eef-91cd-d1cb8be35673"
    ]
))

IAMRole3 = template.add_resource(iam.Role(
    'IAMRole3',
    Path="/",
    RoleName="s3-erjan",
    AssumeRolePolicyDocument="{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"s3.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}",
    MaxSessionDuration=3600,
    ManagedPolicyArns=[
        "arn:aws:iam::aws:policy/TranslateReadOnly",
        "arn:aws:iam::aws:policy/TranslateFullAccess"
    ],
    Description="Allows S3 to call AWS services on your behalf."
))

IAMRole4 = template.add_resource(iam.Role(
    'IAMRole4',
    Path="/service-role/",
    RoleName="results-role-cs7bdnlc",
    AssumeRolePolicyDocument="{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"lambda.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}",
    MaxSessionDuration=3600,
    ManagedPolicyArns=[
        Ref(IAMManagedPolicy10),
        Ref(IAMManagedPolicy3),
        "arn:aws:iam::025416187662:policy/service-role/AWSLambdaVPCAccessExecutionRole-716e4420-886d-452b-a2b9-d916cd7edcde",
        "arn:aws:iam::aws:policy/AWSLambdaInvocation-DynamoDB",
        "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
    ]
))

IAMRole5 = template.add_resource(iam.Role(
    'IAMRole5',
    Path="/",
    RoleName="sqs_apigateway_role",
    AssumeRolePolicyDocument="{\"Version\":\"2012-10-17\",\"Statement\":[{\"Sid\":\"\",\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"apigateway.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}",
    MaxSessionDuration=3600,
    ManagedPolicyArns=[
        "arn:aws:iam::aws:policy/service-role/AmazonAPIGatewayPushToCloudWatchLogs",
        "arn:aws:iam::aws:policy/AmazonSQSFullAccess"
    ],
    Description="Allows API Gateway to push logs to CloudWatch Logs."
))

IAMRole6 = template.add_resource(iam.Role(
    'IAMRole6',
    Path="/",
    RoleName="vote-processor-ec2-role",
    AssumeRolePolicyDocument="{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"ec2.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}",
    MaxSessionDuration=3600,
    ManagedPolicyArns=[
        Ref(IAMManagedPolicy7),
        Ref(IAMManagedPolicy5)
    ],
    Description="vote processor can receive from sqs and send messages to dynamodb"
))

IAMRole7 = template.add_resource(iam.Role(
    'IAMRole7',
    Path="/service-role/",
    RoleName="vote_processor_ec2-role-6r4x3dcf",
    AssumeRolePolicyDocument="{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"lambda.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}",
    MaxSessionDuration=3600,
    ManagedPolicyArns=[
        Ref(IAMManagedPolicy7),
        Ref(IAMManagedPolicy5),
        "arn:aws:iam::025416187662:policy/service-role/AWSLambdaBasicExecutionRole-6cc57b7a-0289-4b56-a380-d0731b195cf5"
    ]
))

IAMRole8 = template.add_resource(iam.Role(
    'IAMRole8',
    Path="/service-role/",
    RoleName="voting-role-z6z0brhg",
    AssumeRolePolicyDocument="{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"lambda.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}",
    MaxSessionDuration=3600,
    ManagedPolicyArns=[
        Ref(IAMManagedPolicy6),
        "arn:aws:iam::025416187662:policy/service-role/AWSLambdaVPCAccessExecutionRole-716e4420-886d-452b-a2b9-d916cd7edcde",
        "arn:aws:iam::025416187662:policy/service-role/AWSLambdaBasicExecutionRole-427c92eb-1f05-4b19-b56b-5a9a21c52886"
    ]
))

IAMRole9 = template.add_resource(iam.Role(
    'IAMRole9',
    Path="/service-role/",
    RoleName="voting-role-tiym3gs8",
    AssumeRolePolicyDocument="{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"lambda.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}",
    MaxSessionDuration=3600,
    ManagedPolicyArns=[
        Ref(IAMManagedPolicy2),
        "arn:aws:iam::025416187662:policy/service-role/AWSLambdaSNSTopicDestinationExecutionRole-b1f9acb5-8c51-4416-9acd-2a62c7d445fc",
        Ref(IAMManagedPolicy4)
    ]
))

IAMServiceLinkedRole = template.add_resource(iam.ServiceLinkedRole(
    'IAMServiceLinkedRole',
    AWSServiceName="ops.apigateway.amazonaws.com",
    Description="The Service Linked Role is used by Amazon API Gateway."
))

IAMManagedPolicy = template.add_resource(iam.ManagedPolicy(
    'IAMManagedPolicy',
    ManagedPolicyName="AWSLambdaBasicExecutionRole-26905855-e012-4435-a907-3405124b0309",
    Path="/service-role/",
    PolicyDocument="""        {
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
"""
))

IAMManagedPolicy2 = template.add_resource(iam.ManagedPolicy(
    'IAMManagedPolicy2',
    ManagedPolicyName="AWSLambdaBasicExecutionRole-b4e0f21f-4840-4bfa-b6e1-e0f9b62c73c7",
    Path="/service-role/",
    PolicyDocument="""        {
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
"""
))

IAMManagedPolicy3 = template.add_resource(iam.ManagedPolicy(
    'IAMManagedPolicy3',
    ManagedPolicyName="AWSLambdaBasicExecutionRole-dbca2dcf-f8e8-49d6-bb7c-5ff50e1c8cef",
    Path="/service-role/",
    PolicyDocument="""        {
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
"""
))

IAMManagedPolicy4 = template.add_resource(iam.ManagedPolicy(
    'IAMManagedPolicy4',
    ManagedPolicyName="AWSLambdaVPCAccessExecutionRole-3a7912c6-f863-4299-b9d1-3a29dd14736e",
    Path="/service-role/",
    PolicyDocument="""        {
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
"""
))

IAMManagedPolicy5 = template.add_resource(iam.ManagedPolicy(
    'IAMManagedPolicy5',
    ManagedPolicyName="ec2-can-access-sqs",
    Path="/",
    PolicyDocument="""        {
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
"""
))

IAMManagedPolicy6 = template.add_resource(iam.ManagedPolicy(
    'IAMManagedPolicy6',
    ManagedPolicyName="voting-backend-can-send-to-sns",
    Path="/",
    PolicyDocument="""        {
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
"""
))

IAMManagedPolicy7 = template.add_resource(iam.ManagedPolicy(
    'IAMManagedPolicy7',
    ManagedPolicyName="ec2-can-access-dynamodb",
    Path="/",
    PolicyDocument="""        {
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
"""
))

IAMManagedPolicy8 = template.add_resource(iam.ManagedPolicy(
    'IAMManagedPolicy8',
    ManagedPolicyName="dynamodb_access_votes",
    Path="/",
    PolicyDocument="""        {
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
"""
))

IAMManagedPolicy9 = template.add_resource(iam.ManagedPolicy(
    'IAMManagedPolicy9',
    ManagedPolicyName="votes-test-dynamodb-lambda-get-item-policy",
    Path="/",
    PolicyDocument="""        {
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
"""
))

IAMManagedPolicy10 = template.add_resource(iam.ManagedPolicy(
    'IAMManagedPolicy10',
    ManagedPolicyName="lambda_invoke_dynamodb_get_item",
    Path="/",
    PolicyDocument="""        {
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
"""
))

IAMManagedPolicy11 = template.add_resource(iam.ManagedPolicy(
    'IAMManagedPolicy11',
    ManagedPolicyName="sqs-erjan-my-vote",
    Path="/",
    PolicyDocument="""        {
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
"""
))

IAMInstanceProfile = template.add_resource(iam.InstanceProfile(
    'IAMInstanceProfile',
    Path="/",
    InstanceProfileName=Ref(IAMRole6),
    Roles=[
        Ref(IAMRole6)
    ]
))

IAMAccessKey = template.add_resource(iam.AccessKey(
    'IAMAccessKey',
    Status="Active",
    UserName="admin"
))

IAMAccessKey2 = template.add_resource(iam.AccessKey(
    'IAMAccessKey2',
    Status="Active",
    UserName="former2-iac-generator"
))

EC2Volume = template.add_resource(ec2.Volume(
    'EC2Volume',
    AvailabilityZone=GetAtt(EC2Instance, 'AvailabilityZone'),
    Encrypted=False,
    Size=8,
    VolumeType="gp2",
    SnapshotId="snap-097c82c1f068b49cb",
    MultiAttachEnabled=False
))

EC2NetworkInterface = template.add_resource(ec2.NetworkInterface(
    'EC2NetworkInterface',
    Description="AWS Lambda VPC ENI-voting-434f3861-dec2-41e2-8871-aba9fbb9d218",
    PrivateIpAddress="10.0.0.45",
    PrivateIpAddresses=[
        ec2.PrivateIpAddressSpecification(
            PrivateIpAddress="10.0.0.45",
            Primary=True
        )
    ],
    SubnetId=Ref(EC2Subnet),
    SourceDestCheck=True,
    GroupSet=[
        "sg-01afc2eba5b520f9b"
    ]
))

EC2NetworkInterface2 = template.add_resource(ec2.NetworkInterface(
    'EC2NetworkInterface2',
    Description="",
    PrivateIpAddress=GetAtt(EC2Instance, 'PrivateIp'),
    PrivateIpAddresses=[
        ec2.PrivateIpAddressSpecification(
            PrivateIpAddress=GetAtt(EC2Instance, 'PrivateIp'),
            Primary=True
        )
    ],
    SubnetId=Ref(EC2Subnet),
    SourceDestCheck=True,
    GroupSet=[
        "sg-01afc2eba5b520f9b"
    ]
))

EC2NetworkInterfaceAttachment = template.add_resource(ec2.NetworkInterfaceAttachment(
    'EC2NetworkInterfaceAttachment',
    NetworkInterfaceId="eni-04c7a8adb7484ca50",
    DeviceIndex=0,
    InstanceId=Ref(EC2Instance),
    DeleteOnTermination=True
))

EC2VPCCidrBlock = template.add_resource(ec2.VPCCidrBlock(
    'EC2VPCCidrBlock',
    VpcId=Ref(EC2VPC),
    Ipv6CidrBlock="2600:1f10:4453:6100::/56",
    Ipv6Pool="Amazon"
))

EC2Subnet = template.add_resource(ec2.Subnet(
    'EC2Subnet',
    AvailabilityZone="us-east-1d",
    CidrBlock=GetAtt(EC2VPC, 'CidrBlock'),
    VpcId=Ref(EC2VPC),
    MapPublicIpOnLaunch=False,
    Tags=[
        {
            "Key": "Name",
            "Value": "subnet1"
        }
    ]
))

EC2InternetGateway = template.add_resource(ec2.InternetGateway(
    'EC2InternetGateway',
    Tags=[
        {
            "Key": "Name",
            "Value": "ll"
        }
    ]
))

EC2EIP = template.add_resource(ec2.EIP(
    'EC2EIP',
    Domain="vpc"
))

EC2Route = template.add_resource(ec2.Route(
    'EC2Route',
    DestinationCidrBlock="0.0.0.0/0",
    GatewayId=Ref(EC2InternetGateway),
    RouteTableId=Ref(EC2RouteTable)
))

EC2RouteTable = template.add_resource(ec2.RouteTable(
    'EC2RouteTable',
    VpcId=Ref(EC2VPC)
))

print(template.to_yaml())
