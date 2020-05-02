resource "aws_lambda_function" "save_reading" {
  filename         = "../../lambda/zip/save_reading.zip"
  function_name    = "dirtbag-save-soil-reading"
  role             = aws_iam_role.save_reading.arn
  handler          = "save_reading.lambda_handler"
  runtime          = "python3.7"
  source_code_hash = filebase64sha256("../../lambda/zip/save_reading.zip")
  timeout = 10
}

resource "aws_lambda_function" "render_index" {
  filename         = "../../lambda/zip/render_index.zip"
  function_name    = "dirtbag-render-index"
  role             = aws_iam_role.render_index.arn
  handler          = "render_index.lambda_handler"
  runtime          = "python3.7"
  source_code_hash = filebase64sha256("../../lambda/zip/render_index.zip")
  layers = [aws_lambda_layer_version.plotly_layer.arn]
  timeout = 30
  memory_size = 256
}

resource "aws_lambda_layer_version" "plotly_layer" {
  layer_name = "plotly-layer"
  filename = "../../lambda/plotly-layer/plotly_layer.zip"
  compatible_runtimes = ["python3.6", "python3.7"]
}

resource "aws_lambda_event_source_mapping" "example" {
  event_source_arn  = aws_dynamodb_table.dirtbag-dynamodb-table.stream_arn
  function_name     = aws_lambda_function.render_index.arn
  starting_position = "LATEST"
}