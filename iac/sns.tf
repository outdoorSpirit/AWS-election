
# ###########################################
# #SNS creation
# ###########################################

resource "aws_sns_topic" "vote_sns" {
  name = var.sns_name
}

resource "aws_sns_topic_policy" "vote_sns_access_policy" {
  arn = aws_sns_topic.vote_sns.arn

  policy = data.aws_iam_policy_document.vote_sns_access_policy.json
}

data "aws_iam_policy_document" "vote_sns_access_policy" {
  policy_id = "__default_policy_ID"

  statement {
    actions = [
      "SNS:Publish",
      "SNS:RemovePermission",
      "SNS:SetTopicAttributes",
      "SNS:DeleteTopic",
      "SNS:ListSubscriptionsByTopic",
      "SNS:GetTopicAttributes",
      "SNS:AddPermission",
      "SNS:Subscribe"
    ]

    condition {
      test     = "StringEquals"
      variable = "AWS:SourceOwner"

      values = [
        var.account_id
      ]
    }

    effect = "Allow"

    principals {
      type        = "AWS"
      identifiers = ["*"]
    }

    resources = [
      aws_sns_topic.vote_sns.arn
    ]

    sid = "__default_statement_ID"
  }

  statement {
    sid       = "__console_pub_0"
    actions   = ["SNS:Publish"]
    resources = [aws_sns_topic.vote_sns.arn]
    principals {
      type        = "AWS"
      identifiers = ["*"]
    }
    effect = "Allow"

  }

  statement {
    sid       = "__console_sub_0"
    actions   = ["SNS:Subscribe"]
    resources = [aws_sns_topic.vote_sns.arn]
    principals {
      type        = "AWS"
      identifiers = ["*"]
    }
    effect = "Allow"

  }

}

output "sns_arn_erjan" {
  value       = aws_sns_topic.vote_sns.arn
  description = "aws full sns topic"
}


resource "aws_sns_topic_subscription" "sns_vote_sqs_subscription" {
  topic_arn            = aws_sns_topic.vote_sns.arn
  protocol             = "sqs"
  endpoint             = aws_sqs_queue.sqs_vote.arn
  raw_message_delivery = "true"

  depends_on = [
    aws_sqs_queue.sqs_vote
  ]
}


