resource "aws_lambda_permission" "api_gw_save_reading" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.save_reading.function_name
  principal     = "apigateway.amazonaws.com"

  # More: http://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-control-access-using-iam-policies-to-invoke-api.html
  source_arn = "arn:aws:execute-api:${data.aws_region.current.name}:${var.accountId}:${aws_api_gateway_rest_api.save_reading_api.id}/*/${aws_api_gateway_method.save_reading_post_method.http_method}${aws_api_gateway_resource.resource.path}"
}

resource "aws_lambda_function" "save_reading" {
  filename      = "../../lambda/zip/save_reading.zip"
  function_name = "dirtbag-save-soil-reading"
  role          = aws_iam_role.save_reading_role.arn
  handler       = "save_reading.lambda_handler"
  runtime       = "python3.7"

  # The filebase64sha256() function is available in Terraform 0.11.12 and later
  # For Terraform 0.11.11 and earlier, use the base64sha256() function and the file() function:
  # source_code_hash = "${base64sha256(file("lambda.zip"))}"
  source_code_hash = filebase64sha256("../../lambda/zip/save_reading.zip")
}
