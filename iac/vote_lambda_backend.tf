


# ###########################################
# # VOTE lambda backend 
# ###########################################

# terraform import aws_iam_role.vote_lambda_iam_role iam_for_lambda

resource "aws_iam_role" "vote_lambda_iam_role" {


  name               = "voting_role"
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

resource "aws_iam_policy" "log_policy" {

  name   = "log_policy"
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

resource "aws_iam_role_policy_attachment" "attach_log_policy_to_iam_role" {
  role       = aws_iam_role.vote_lambda_iam_role.name
  policy_arn = aws_iam_policy.log_policy.arn
}

resource "aws_iam_policy" "vote_lambda_policy_send_to_sns" {

  name   = "vote_lambda_policy_send_to_sns"
  policy = data.aws_iam_policy_document.vote_lambda_policy_send_to_sns.json
}

data "aws_iam_policy_document" "vote_lambda_policy_send_to_sns" {
  statement {
    sid = ""

    actions = [
      "sns:Publish"
    ]
    resources = ["${aws_sns_topic.vote_sns.arn}"]
  }
}

resource "aws_iam_role_policy_attachment" "attach_sns_send_to_iam_role" {
  role       = aws_iam_role.vote_lambda_iam_role.name
  policy_arn = aws_iam_policy.vote_lambda_policy_send_to_sns.arn
}

data "archive_file" "zip_the_python_code" {
  type        = "zip"
  source_file = "${path.module}/voting.py"
  output_path = "${path.module}/voting.zip"
}


resource "aws_lambda_function" "vote_lambda_backend" {
  filename      = "${path.module}/voting.zip"
  function_name = "voting"
  role          = aws_iam_role.vote_lambda_iam_role.arn
  handler       = "voting.lambda_handler"
  runtime       = "python3.9"
  depends_on    = [aws_iam_role_policy_attachment.attach_sns_send_to_iam_role]

  environment {
    variables = {
      SNS_ARN    = aws_sns_topic.vote_sns.arn,
      def_region = "${var.def_region}"
    }
  }
}


resource "aws_lambda_function_event_invoke_config" "vote_sns_trigger_lambda_event_invoke_config" {
  function_name = aws_lambda_function.vote_lambda_backend.function_name

  destination_config {

    on_success {
      destination = aws_sns_topic.vote_sns.arn
    }


  }
}








