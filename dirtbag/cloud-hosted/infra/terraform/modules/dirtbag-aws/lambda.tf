resource "aws_lambda_function" "save_reading" {
  filename         = "${var.lambda_dir_path}/zip/save_reading.zip"
  function_name    = "${var.instantiation_name}-save-soil-reading"
  role             = aws_iam_role.save_reading.arn
  handler          = "save_reading.lambda_handler"
  runtime          = "python3.7"
  source_code_hash = filebase64sha256("${var.lambda_dir_path}/zip/save_reading.zip")
  timeout = 10

    environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.dirtbag-dynamodb-table.name
    }
  }
}

resource "aws_lambda_function" "render_index" {
  filename         = "${var.lambda_dir_path}/zip/render_index.zip"
  function_name    = "${var.instantiation_name}-render-index"
  role             = aws_iam_role.render_index.arn
  handler          = "render_index.lambda_handler"
  runtime          = "python3.7"
  source_code_hash = filebase64sha256("${var.lambda_dir_path}/zip/render_index.zip")
  layers = [aws_lambda_layer_version.plotly_layer.arn]
  timeout = 30
  memory_size = 256

  environment {
    variables = {
      OUTPUT_BUCKET = aws_s3_bucket.index.id
      TABLE_NAME = aws_dynamodb_table.dirtbag-dynamodb-table.name
    }
  }

}

resource "aws_lambda_layer_version" "plotly_layer" {
  layer_name = "${var.instantiation_name}-plotly-layer"
  filename = "${var.lambda_dir_path}/plotly-layer/plotly_layer.zip"
  compatible_runtimes = ["python3.6", "python3.7"]
}

resource "aws_lambda_event_source_mapping" "lambda_dynamo_event_mapping" {
  event_source_arn  = aws_dynamodb_table.dirtbag-dynamodb-table.stream_arn
  function_name     = aws_lambda_function.render_index.arn
  starting_position = "LATEST"
}
