resource "aws_cognito_user_pool" "cognito-user-pool" {
  name = "${var.instantiation_name}-cognito-user-pool"

  admin_create_user_config {
    allow_admin_create_user_only = true
  }

}

resource "aws_cognito_identity_pool" "cognito-id-pool" {
  identity_pool_name = "${replace(var.instantiation_name, "-", " ")} cognito id pool"
  allow_unauthenticated_identities = false

  cognito_identity_providers {
    client_id = aws_cognito_user_pool.cognito-user-pool.id
    provider_name = aws_cognito_user_pool.cognito-user-pool.name
    server_side_token_check = false
  }
}
