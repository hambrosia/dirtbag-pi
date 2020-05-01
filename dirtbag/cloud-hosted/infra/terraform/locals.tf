locals {
  environment = terraform.workspace

  save_reading_api_gw_arn = "arn:aws:execute-api:${data.aws_region.current.name}:${var.accountId}:${aws_api_gateway_rest_api.save_reading_api.id}/*/${aws_api_gateway_method.save_reading_post_method.http_method}${aws_api_gateway_resource.save_reading_api.path}"

  save_reading_api_gw_stage_name = "dirtbag-${terraform.workspace}"

  save_reading_uri = " ${aws_api_gateway_deployment.save_reading_deployment.invoke_url}/${aws_api_gateway_resource.save_reading_api.path_part}"

}

data "aws_region" "current" {}
