resource "aws_cognito_user_pool" "cognito_user_pool" {
  name = "${var.instantiation_name}-cognito-user-pool"

  admin_create_user_config {
    allow_admin_create_user_only = true
  }

}


# TODO: Fix the identity, needs a client resource
resource "aws_cognito_identity_pool" "cognito_id_pool" {
  identity_pool_name = "dirtbag"
  allow_unauthenticated_identities = false

//  cognito_identity_providers {
//    client_id = aws_cognito_user_pool.cognito_user_pool.id
//    provider_name = aws_cognito_user_pool.cognito_user_pool.name
//    server_side_token_check = false
//  }
}
