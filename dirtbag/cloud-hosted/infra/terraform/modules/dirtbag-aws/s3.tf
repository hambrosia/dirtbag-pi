resource "aws_s3_bucket" "index" {
  bucket_prefix = local.graph_prefix
  acl    = "public-read"

  website {
    index_document = "index.html"
    error_document = "error.html"
  }

  force_destroy = true

}

resource "aws_s3_bucket_policy" "index" {
  bucket = aws_s3_bucket.index.id
  policy = data.aws_iam_policy_document.graph_bucket_public.json
}

