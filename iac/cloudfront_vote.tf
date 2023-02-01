

###########################################
# cloudfront vote creation
###########################################

resource "aws_cloudfront_distribution" "cloudfront_vote" {

  default_root_object = "index.html"

  origin {
    domain_name = aws_s3_bucket.frontend_vote.bucket_regional_domain_name
    origin_id   = aws_s3_bucket.frontend_vote.id
    origin_path = ""
    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.frontend_vote_cloudfront_oai.cloudfront_access_identity_path
    }
  }

  default_cache_behavior {
    allowed_methods        = ["HEAD", "GET", "OPTIONS"]
    cached_methods         = ["HEAD", "GET", "OPTIONS"]
    target_origin_id       = aws_s3_bucket.frontend_vote.id
    viewer_protocol_policy = "allow-all"

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }


  }
  comment     = "VOTE"
  price_class = "PriceClass_All"
  enabled     = true
  viewer_certificate {
    cloudfront_default_certificate = true
    minimum_protocol_version       = "TLSv1"
    ssl_support_method             = "vip"
  }
  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
  http_version = "http2"

  depends_on = [
    aws_cloudfront_origin_access_identity.frontend_vote_cloudfront_oai, aws_s3_bucket.frontend_vote
  ]
}


resource "aws_cloudfront_origin_request_policy" "cloudfront_vote_origin_request_policy" {
  name = "cloudfront_vote_origin_request_policy"

  cookies_config {
    cookie_behavior = "none"
  }
  headers_config {
    header_behavior = "none"
  }
  query_strings_config {
    query_string_behavior = "none"
  }

  depends_on = [aws_cloudfront_distribution.cloudfront_vote]
}

resource "aws_cloudfront_cache_policy" "cloudfront_vote_cache_policy" {
  name        = "cloudfront_vote_cache_policy"
  default_ttl = 86400
  max_ttl     = 31536000
  min_ttl     = 1
  parameters_in_cache_key_and_forwarded_to_origin {
    cookies_config {
      cookie_behavior = "none"
    }
    headers_config {
      header_behavior = "whitelist"
      headers {
        items = ["origin", "access-control-request-headers", "access-control-request-method"]
      }
    }
    query_strings_config {
      query_string_behavior = "none"
    }
    enable_accept_encoding_brotli = true
    enable_accept_encoding_gzip   = true
  }

  depends_on = [aws_cloudfront_distribution.cloudfront_vote]

}

resource "aws_cloudfront_response_headers_policy" "cloudfront_vote_response_headers_policy" {
  name = "cloudfront_vote_response_headers_policy"

  cors_config {
    access_control_allow_credentials = false

    access_control_allow_headers {
      items = ["*"]
    }

    access_control_allow_methods {
      items = ["GET", "HEAD", "PUT", "POST", "PATCH", "DELETE", "OPTIONS"]
    }

    access_control_allow_origins {
      items = ["*"]
    }
    access_control_expose_headers {
      items = ["*"]
    }

    origin_override = false
  }

  depends_on = [aws_cloudfront_distribution.cloudfront_vote]

}


output "cf_vote_domain_name" {

  value       = aws_cloudfront_distribution.cloudfront_vote.domain_name
  description = "vote cloudfront URL"
}