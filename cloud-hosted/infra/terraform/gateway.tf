resource "aws_api_gateway_rest_api" "save_reading_api" {
  name = "dirtbag-pi-save-reading"
}

resource "aws_api_gateway_resource" "resource" {
  path_part   = "resource"
  parent_id   = aws_api_gateway_rest_api.save_reading_api.root_resource_id
  rest_api_id = aws_api_gateway_rest_api.save_reading_api.id
}

resource "aws_api_gateway_method" "save_reading_post_method" {
  rest_api_id   = aws_api_gateway_rest_api.save_reading_api.id
  resource_id   = aws_api_gateway_resource.resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "save_reading_integration" {
  rest_api_id             = aws_api_gateway_rest_api.save_reading_api.id
  resource_id             = aws_api_gateway_resource.resource.id
  http_method             = aws_api_gateway_method.save_reading_post_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.save_reading.invoke_arn
}

resource "aws_api_gateway_deployment" "save_reading_deployment" {
  depends_on = [aws_api_gateway_integration.save_reading_integration]

  rest_api_id = aws_api_gateway_rest_api.save_reading_api.id
  stage_name  = terraform.workspace

}