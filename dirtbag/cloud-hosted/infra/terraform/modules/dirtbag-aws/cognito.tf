resource "aws_cognito_user_pool" "dirtbag_user_pool" {
  name = "${var.instantiation_name}-cognito-user-pool"

  admin_create_user_config {
    allow_admin_create_user_only = true
  }

}

resource "aws_cognito_user_pool_client" "dirtbag_ui_app_client" {
  name = "${var.instantiation_name}-ui-app-client"
  user_pool_id = aws_cognito_user_pool.dirtbag_user_pool.id
}

