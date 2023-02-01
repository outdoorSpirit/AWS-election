
###########################################
#S3 VOTE bucket creation
###########################################

resource "aws_s3_bucket" "frontend_vote" {
  bucket = "frontend-bucket-${var.vote}-${var.def_region}"
}

resource "aws_s3_bucket_policy" "frontend_vote_s3_bucket_policy" {
  bucket     = aws_s3_bucket.frontend_vote.id
  policy     = data.aws_iam_policy_document.frontend_vote_s3_bucket_policy.json
  depends_on = [aws_s3_bucket.frontend_vote]

}

data "aws_iam_policy_document" "frontend_vote_s3_bucket_policy" {
  statement {
    sid = "PublicReadGetObject"

    principals {
      type        = "*"
      identifiers = ["*"]
    }

    actions = [
      "s3:GetObject"
    ]

    resources = ["${aws_s3_bucket.frontend_vote.arn}/*"]

  }

  statement {
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.frontend_vote.arn}/*"]

    principals {
      type        = "AWS"
      identifiers = [aws_cloudfront_origin_access_identity.frontend_vote_cloudfront_oai.iam_arn]
    }
  }

}

resource "aws_cloudfront_origin_access_identity" "frontend_vote_cloudfront_oai" {
  comment    = "frontend_vote origin"
  depends_on = [aws_s3_bucket.frontend_vote]
}

resource "aws_s3_bucket_ownership_controls" "frontend_vote-bucket-ownership" {
  bucket = aws_s3_bucket.frontend_vote.id

  rule {
    object_ownership = "BucketOwnerEnforced"
  }

  depends_on = [aws_s3_bucket.frontend_vote]
}



resource "aws_s3_bucket_website_configuration" "frontend_vote-static" {
  bucket = aws_s3_bucket.frontend_vote.bucket

  index_document {
    suffix = "index.html"
  }

  depends_on = [aws_s3_bucket.frontend_vote, aws_s3_object.index_file_vote]

}



resource "aws_s3_object" "index_file_vote" {
  bucket       = aws_s3_bucket.frontend_vote.id
  key          = "index.html"
  content_type = "text/html"
  content = templatefile("./vote/index.html.tpl", {
    backend_api_gateway = aws_apigatewayv2_stage.default.invoke_url
  })

  depends_on = [aws_s3_bucket.frontend_vote, aws_apigatewayv2_api.main_apigateway]
}

resource "aws_s3_object" "myicon_vote" {
  bucket       = aws_s3_bucket.frontend_vote.id
  key          = "myicon.png"
  source       = "./vote/myicon.png"
  content_type = "image/png"

  depends_on = [aws_s3_bucket.frontend_vote]

}

resource "aws_s3_object" "stylecss_vote" {
  bucket       = aws_s3_bucket.frontend_vote.id
  key          = "style.css"
  source       = "./vote/style.css"
  content_type = "text/css"

  depends_on = [aws_s3_bucket.frontend_vote]
}

