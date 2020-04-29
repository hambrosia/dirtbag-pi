resource "aws_lambda_permission" "api_gw_save_reading" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.save_reading.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = local.save_reading_api_gw_arn
}

resource "aws_lambda_function" "save_reading" {
  filename         = "../../lambda/zip/save_reading.zip"
  function_name    = "dirtbag-save-soil-reading"
  role             = aws_iam_role.save_reading_role.arn
  handler          = "save_reading.lambda_handler"
  runtime          = "python3.7"
  source_code_hash = filebase64sha256("../../lambda/zip/save_reading.zip")
}
