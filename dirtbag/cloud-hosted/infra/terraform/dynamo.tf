resource "aws_dynamodb_table" "dirtbag-dynamodb-table" {
  name         = "DirtbagReadings"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "uuid"
  range_key    = "timestamp"

  attribute {
    name = "uuid"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "S"
  }

  ttl {
    attribute_name = "TimeToExist"
    enabled        = false
  }

  tags = {
    Name        = "dirtbag-pi-dynamo-table"
    Environment = local.environment
  }
}