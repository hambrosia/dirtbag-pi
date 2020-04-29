output "client_key" {
  value = aws_iam_access_key.dirtbag_client.encrypted_secret
}