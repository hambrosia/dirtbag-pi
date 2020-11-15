output "cient_key" {
  value = aws_iam_access_key.dirtbag_client.id
}

output "client_secret" {
  value = aws_iam_access_key.dirtbag_client.secret
}

output "index_url" {
  value = aws_s3_bucket.index.website_endpoint
}

output "web_ui_config_json" {
  value = jsonencode({
    "cognito" : {
      "REGION" : data.aws_region.current.id,
      "USER_POOL_ID" : aws_cognito_user_pool.dirtbag_user_pool.id,
      "APP_CLIENT_ID" : aws_cognito_user_pool_client.dirtbag_ui_app_client.id
    },
    "s3" : {
      "BUCKET_NAME" : aws_s3_bucket.index.id,
      "REGION" : data.aws_region.current.id
    }
  })

}