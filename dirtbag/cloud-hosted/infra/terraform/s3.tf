resource "aws_s3_bucket" "index" {
  bucket = "dirtbag-public-index"
  acl    = "public-read"

  website {
    index_document = "index.html"
    error_document = "error.html"
  }
}