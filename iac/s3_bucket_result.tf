

###########################################
#S3 RESULT bucket creation
###########################################

resource "aws_s3_bucket" "frontend_result" {
  bucket = "frontend-bucket-${var.result}-${var.def_region}"

}

resource "aws_s3_bucket_policy" "frontend_result_s3_bucket_policy" {
  bucket     = aws_s3_bucket.frontend_result.id
  policy     = data.aws_iam_policy_document.frontend_result_s3_bucket_policy.json
  depends_on = [aws_s3_bucket.frontend_result]

}

data "aws_iam_policy_document" "frontend_result_s3_bucket_policy" {
  statement {
    sid = "PublicReadGetObject"

    principals {
      type        = "*"
      identifiers = ["*"]
    }

    actions = [
      "s3:GetObject"
    ]

    resources = ["${aws_s3_bucket.frontend_result.arn}/*"]

  }

  statement {
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.frontend_result.arn}/*"]

    principals {
      type        = "AWS"
      identifiers = [aws_cloudfront_origin_access_identity.frontend_result_cloudfront_oai.iam_arn]
    }
  }

}

resource "aws_cloudfront_origin_access_identity" "frontend_result_cloudfront_oai" {
  comment    = "frontend_result origin"
  depends_on = [aws_s3_bucket.frontend_result]
}



resource "aws_s3_bucket_ownership_controls" "frontend_result_bucket_ownership" {
  bucket = aws_s3_bucket.frontend_result.id

  rule {
    object_ownership = "BucketOwnerEnforced"
  }

  depends_on = [aws_s3_bucket.frontend_result]

}


resource "aws_s3_bucket_website_configuration" "frontend_result_static" {
  bucket = aws_s3_bucket.frontend_result.bucket

  index_document {
    suffix = "index.html"
  }

  depends_on = [aws_s3_bucket.frontend_result, aws_s3_object.index_file_result]

}






resource "aws_s3_object" "index_file_result" {
  bucket       = aws_s3_bucket.frontend_result.id
  key          = "index.html"
  source       = "./result/index.html"
  content_type = "text/html"

  depends_on = [aws_s3_bucket.frontend_result]

}

resource "aws_s3_object" "myicon_result" {
  bucket       = aws_s3_bucket.frontend_result.id
  key          = "myicon.png"
  source       = "./result/myicon.png"
  content_type = "image/png"

  depends_on = [aws_s3_bucket.frontend_result]

}

resource "aws_s3_object" "stylecss_result" {
  bucket       = aws_s3_bucket.frontend_result.id
  key          = "style.css"
  source       = "./result/style.css"
  content_type = "text/css"


  depends_on = [aws_s3_bucket.frontend_result]

}


resource "aws_s3_object" "appjs" {
  bucket       = aws_s3_bucket.frontend_result.id
  key          = "app.js"
  content_type = "text/html"

  content = templatefile("./result/app.js.tpl", {
    backend_api_gateway = aws_apigatewayv2_stage.default.invoke_url
  })
  depends_on = [aws_s3_bucket.frontend_result]

}



