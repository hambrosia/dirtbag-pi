locals {
  environment             = terraform.workspace

  save_reading_api_gw_arn = "arn:aws:execute-api:${data.aws_region.current.name}:${var.accountId}:${aws_api_gateway_rest_api.save_reading_api.id}/*/${aws_api_gateway_method.save_reading_post_method.http_method}${aws_api_gateway_resource.save_reading_api.path}"
}

data "aws_region" "current" {}
