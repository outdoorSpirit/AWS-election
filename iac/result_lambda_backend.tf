

# ###########################################
# # RESULT lambda backend 
# ###########################################



resource "aws_iam_role" "result_lambda_iam_role" {
  name               = "result_lambda_iam_role"
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

resource "aws_iam_policy" "result_log_policy" {

  name   = "result_log_policy"
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

resource "aws_iam_role_policy_attachment" "attach_result_log_policy_to_iam_role" {
  role       = aws_iam_role.result_lambda_iam_role.name
  policy_arn = aws_iam_policy.result_log_policy.arn
}


resource "aws_iam_policy" "result_dynamodb_get_item_policy" {

  name   = "result_dynamodb_get_item_policy"
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
            "Resource": "${aws_dynamodb_table.dynamodb_table_votes.arn}"
        }
    ]
}
EOF
}



resource "aws_iam_role_policy_attachment" "attach_result_dynamodb_get_item_policy" {
  role       = aws_iam_role.result_lambda_iam_role.name
  policy_arn = aws_iam_policy.result_dynamodb_get_item_policy.arn
}



data "archive_file" "result_zip_code" {
  type        = "zip"
  source_file = "${path.module}/result.py"
  output_path = "${path.module}/result.zip"
}


resource "aws_lambda_function" "result_lambda_backend" {
  filename      = "${path.module}/result.zip"
  function_name = "results"
  role          = aws_iam_role.result_lambda_iam_role.arn
  handler       = "result.lambda_handler"
  runtime       = "python3.9"


  environment {
    variables = {

      dynamodb_table_name    = "${var.dynamodb_table_name}",
      dynamodb_partition_key = "${var.dynamodb_partition_key}",
      dynamodb_field         = "${var.dynamodb_field}"

    }
  }

}


