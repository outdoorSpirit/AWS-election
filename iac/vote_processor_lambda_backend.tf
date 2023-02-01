

# ###########################################
# # vote processor lambda backend
# ###########################################


resource "aws_iam_role" "vote_processor_lambda_iam_role" {
  name               = "vote_processor_lambda_iam_role"
  assume_role_policy = <<EOF
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": "sts:AssumeRole",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Effect": "Allow",
                "Sid": ""
            }
        ]
    }
    EOF
}

resource "aws_iam_policy" "vote_processor_log_policy" {

  name   = "vote_processor_log_policy"
  policy = <<EOF
{
 "Version": "2012-10-17",
 "Statement": [
   {
     "Action": [
       "logs:CreateLogGroup",
       "logs:CreateLogStream",
       "logs:PutLogEvents"
     ],
     "Resource": "arn:aws:logs:*:*:*",
     "Effect": "Allow"
   }
 ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "attach_vote_processor_log_policy_to_iam_role" {
  role       = aws_iam_role.vote_processor_lambda_iam_role.name
  policy_arn = aws_iam_policy.vote_processor_log_policy.arn
}


resource "aws_iam_policy" "vote_processor_dynamodb_policy" {


  # source_arn    = "${aws_apigatewayv2_api.main_apigateway.execution_arn}/*/*/results"

  name   = "vote_processor_dynamodb_policy"
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
            "Resource": "${aws_dynamodb_table.dynamodb_table_votes.arn}"
        }
    ]
}
EOF
}


resource "aws_iam_role_policy_attachment" "attach_vote_processor_dynamodb_policy_to_iam_role" {
  role       = aws_iam_role.vote_processor_lambda_iam_role.name
  policy_arn = aws_iam_policy.vote_processor_dynamodb_policy.arn
}


resource "aws_iam_policy" "vote_processor_sqs_policy" {

  name   = "vote_processor_sqs_policy"
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
            "Resource": "${aws_sqs_queue.sqs_vote.arn}"

        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": ["sqs:GetQueueAttributes", "sqs:ReceiveMessage"],
            "Resource": "${aws_sqs_queue.sqs_vote.arn}"

        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "vote_processor_sqs_access_policy" {
  role       = aws_iam_role.vote_processor_lambda_iam_role.name
  policy_arn = aws_iam_policy.vote_processor_sqs_policy.arn
}



data "archive_file" "vote_processor_zip_code" {
  type        = "zip"
  source_file = "${path.module}/vote_processor.py"
  output_path = "${path.module}/vote_processor.zip"
}



# Event source from SQS
resource "aws_lambda_event_source_mapping" "sqs_to_vote_processor_lambda_trigger" {
  event_source_arn = aws_sqs_queue.sqs_vote.arn
  enabled          = true
  function_name    = aws_lambda_function.vote_processor_lambda_backend.arn
  batch_size       = 1
  depends_on       = [aws_lambda_function.vote_processor_lambda_backend, aws_sqs_queue.sqs_vote]
}



resource "aws_lambda_function" "vote_processor_lambda_backend" {
  filename      = "${path.module}/vote_processor.zip"
  function_name = "vote_processor"
  role          = aws_iam_role.vote_processor_lambda_iam_role.arn
  handler       = "vote_processor.lambda_handler"
  runtime       = "python3.9"

  environment {
    variables = {
      region                 = "${var.def_region}",
      sqs_queue_name         = aws_sqs_queue.sqs_vote.name,
      dynamodb_table_name    = "${var.dynamodb_table_name}",
      dynamodb_partition_key = "${var.dynamodb_partition_key}",
      dynamodb_field         = "${var.dynamodb_field}"

    }
  }
}
