output "cient_key" {
  value = aws_iam_access_key.dirtbag_client.id
}

output "client_secret" {
  value = aws_iam_access_key.dirtbag_client.secret
}

output "index_url" {
  value = aws_s3_bucket.index.website_endpoint
}