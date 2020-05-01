resource "aws_dynamodb_table" "dirtbag-dynamodb-table" {
  name         = "DirtbagReadings"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "sensorid"
  range_key    = "timestamp"

  attribute {
    name = "sensorid"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "S"
  }

  tags = {
    Name        = "dirtbag-pi"
    Environment = local.environment
  }
}