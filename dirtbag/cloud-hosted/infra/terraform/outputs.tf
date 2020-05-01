output "cient_key" {
  value = aws_iam_access_key.dirtbag_client.id
}

output "client_secret" {
  value = aws_iam_access_key.dirtbag_client.secret
}

output "save_readings_url" {
  value = local.save_reading_uri
}

output "index_url" {
  value = aws_s3_bucket.index.website_endpoint
}