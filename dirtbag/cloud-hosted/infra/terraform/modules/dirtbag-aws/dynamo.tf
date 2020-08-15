resource "aws_dynamodb_table" "dirtbag-dynamodb-table" {
  name         = local.dynamo_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "sensorid"
  range_key    = "timestamp"
  stream_enabled = true
  stream_view_type = "NEW_IMAGE"

  attribute {
    name = "sensorid"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "S"
  }

  tags = {
    Name        = local.dynamo_table_name
    Environment = local.environment
  }
}