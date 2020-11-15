data "archive_file" "save_reading" {
  source_file = "${path.module}/lambda/save_reading.py"
  output_path = "${path.module}/lambda/save_reading.zip"
  type        = "zip"
}

resource "aws_lambda_function" "save_reading" {
  filename         = data.archive_file.save_reading.output_path
  function_name    = "${var.instantiation_name}-save-soil-reading"
  role             = aws_iam_role.save_reading.arn
  handler          = "save_reading.lambda_handler"
  runtime          = "python3.7"
  source_code_hash = data.archive_file.save_reading.output_base64sha256
  timeout          = 10

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.dirtbag-dynamodb-table.name
    }
  }
}

data "archive_file" "render_index" {
  source_file = "${path.module}/lambda/render_index.py"
  output_path = "${path.module}/lambda/render_index.zip"
  type        = "zip"
}

resource "aws_lambda_function" "render_index" {
  filename         = data.archive_file.render_index.output_path
  function_name    = "${var.instantiation_name}-render-index"
  role             = aws_iam_role.render_index.arn
  handler          = "render_index.lambda_handler"
  runtime          = "python3.7"
  source_code_hash = data.archive_file.render_index.output_base64sha256
  layers           = [aws_lambda_layer_version.plotly_layer.arn]
  timeout          = 30
  memory_size      = 256

  environment {
    variables = {
      OUTPUT_BUCKET = aws_s3_bucket.index.id
      TABLE_NAME    = aws_dynamodb_table.dirtbag-dynamodb-table.name
    }
  }

}

resource null_resource "make_plotly_layer" {
  provisioner "local-exec" {
    working_dir = "${path.module}/lambda/plotly-layer"
    command     = "mkdir -p python && pip3 install -r requirements.txt -t python && zip -r plotly_layer.zip ./python"
  }
}

resource "aws_lambda_layer_version" "plotly_layer" {
  depends_on          = [null_resource.make_plotly_layer]
  layer_name          = "${var.instantiation_name}-plotly-layer"
  filename            = "${path.module}/lambda/plotly-layer/plotly_layer.zip"
  compatible_runtimes = ["python3.6", "python3.7"]
}

resource "aws_lambda_event_source_mapping" "lambda_dynamo_event_mapping" {
  event_source_arn  = aws_dynamodb_table.dirtbag-dynamodb-table.stream_arn
  function_name     = aws_lambda_function.render_index.arn
  starting_position = "LATEST"
}
