


# ###########################################
# #SQS creation
# ###########################################

resource "aws_sqs_queue" "sqs_vote" {
  name                      = var.sqs_name
  delay_seconds             = 0
  message_retention_seconds = 3000
  receive_wait_time_seconds = 0
  sqs_managed_sse_enabled   = false
}

resource "aws_sqs_queue_policy" "sqs_vote_policy" {
  queue_url = aws_sqs_queue.sqs_vote.id
  policy    = data.aws_iam_policy_document.sqs_vote_policy.json

  depends_on = [
    aws_sqs_queue.sqs_vote
  ]
}


data "aws_iam_policy_document" "sqs_vote_policy" {

  statement {

    sid    = "__owner_statement"
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = ["arn:aws:iam::${var.account_id}:root"]
    }
    actions = ["SQS:*"]

    resources = [aws_sqs_queue.sqs_vote.arn]

  }

  statement {
    sid    = "__consb_0"
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = ["*"]
    }
    actions   = ["SQS:SendMessage"]
    resources = [aws_sqs_queue.sqs_vote.arn]

    condition {
      test     = "ArnLike"
      variable = "aws:SourceArn"

      values = [
        aws_sns_topic.vote_sns.arn
      ]
    }
  }


}

