resource "aws_s3_bucket" "index" {
  bucket_prefix = local.graph_prefix
  acl           = "public-read"

  website {
    index_document = "index.html"
    error_document = "error.html"
  }

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["PUT", "POST", "GET", "DELETE"]
    allowed_origins = ["*"]
    expose_headers  = ["x-amz-server-side-encryption", "x-amz-request-id", "x-amz-id-2", "ETag"]
    max_age_seconds = 3000
  }

  force_destroy = true

}

resource "aws_s3_bucket_policy" "index" {
  bucket = aws_s3_bucket.index.id
  policy = data.aws_iam_policy_document.graph_bucket_public.json
}

