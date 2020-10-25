resource "aws_cognito_user_pool" "dirtbag_user_pool" {
  name = "${var.instantiation_name}-cognito-user-pool"

  verification_message_template {
    default_email_option = "CONFIRM_WITH_LINK"
  }

  auto_verified_attributes = ["email"]
}

resource "aws_cognito_user_pool_domain" "main" {
  domain       = "${var.instantiation_name}-domain"
  user_pool_id = aws_cognito_user_pool.dirtbag_user_pool.id
}

resource "aws_cognito_user_pool_client" "dirtbag_ui_app_client" {
  name = "${var.instantiation_name}-ui-app-client"
  user_pool_id = aws_cognito_user_pool.dirtbag_user_pool.id
}

