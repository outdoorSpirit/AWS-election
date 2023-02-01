

# ###########################################
# # api gateway
# ###########################################

resource "aws_apigatewayv2_api" "main_apigateway" {
  name          = var.apigateway_name
  protocol_type = "HTTP"
  cors_configuration {
    allow_credentials = false
    allow_headers     = ["accept", "content-type"]
    allow_methods = [
      "GET",
      "OPTIONS",
      "POST",
    ]
    allow_origins = [
      # "*",
      "https://${aws_cloudfront_distribution.cloudfront_result.domain_name}",
      "https://${aws_cloudfront_distribution.cloudfront_vote.domain_name}"
    ]
    expose_headers = []
    max_age        = 0
  }
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.main_apigateway.id
  name        = "$default"
  auto_deploy = true
}

# ###########################################
# # VOTE lambda backend integration
# ###########################################

resource "aws_apigatewayv2_integration" "vote_integration" {
  api_id = aws_apigatewayv2_api.main_apigateway.id
  # integration_uri  = aws_lambda_function.vote_lambda_backend.invoke_arn
  integration_uri        = aws_lambda_function.vote_lambda_backend.arn
  integration_type       = "AWS_PROXY"
  payload_format_version = "2.0"

}

resource "aws_apigatewayv2_route" "vote_route" {
  api_id    = aws_apigatewayv2_api.main_apigateway.id
  route_key = "POST /voting"
  target    = "integrations/${aws_apigatewayv2_integration.vote_integration.id}"
}


# resource "aws_iam_role_policy_attachment" "vote_policy_basic_execution_attachment" {
#   role       = aws_iam_role.vote_lambda_iam_role.name
#   policy_arn = "arn:aws:iam:aws:policy/service-role/AWSLambdaBasicExecutionRole"
# }


resource "aws_lambda_permission" "vote_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.vote_lambda_backend.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.main_apigateway.execution_arn}/*/*/voting"
}

# ###########################################
# # RESULT lambda backend integration
# ###########################################

resource "aws_apigatewayv2_integration" "result_integration" {
  api_id = aws_apigatewayv2_api.main_apigateway.id
  # integration_uri  = aws_lambda_function.result_lambda_backend.invoke_arn
  integration_uri        = aws_lambda_function.result_lambda_backend.arn
  integration_type       = "AWS_PROXY"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "result_route" {
  api_id    = aws_apigatewayv2_api.main_apigateway.id
  route_key = "GET /results"
  target    = "integrations/${aws_apigatewayv2_integration.result_integration.id}"
}


resource "aws_lambda_permission" "result_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.result_lambda_backend.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.main_apigateway.execution_arn}/*/*/results"
}



