resource "aws_s3_bucket" "index" {
  bucket_prefix = "dirtbag-graph"
  acl    = "public-read"

  website {
    index_document = "index.html"
    error_document = "error.html"
  }

  force_destroy = true

  policy = <<EOF
{
  "Version": "2008-10-17",
  "Statement": [
    {
      "Sid": "PublicReadForGetBucketObjects",
      "Effect": "Allow",
      "Principal": {
        "AWS": "*"
      },
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::dirtbag-public-index/*"
    }
  ]
}
EOF
}