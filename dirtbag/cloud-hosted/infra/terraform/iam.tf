# Save Reading Lambda Permissions
resource "aws_iam_role" "save_reading_role" {
  name = "dirtbag-save-reading-role"

  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
POLICY
}

resource "aws_iam_policy" "save_reading" {
  name        = "dirtbag-dynamo-write"
  description = "Allow DirtBag Pi Save Reading Lambda to write to Dynamo"

  policy = <<EOF
{
   "Version":"2012-10-17",
   "Statement":[
      {
         "Effect":"Allow",
         "Action":[
            "dynamodb:BatchGet*",
            "dynamodb:DescribeStream",
            "dynamodb:DescribeTable",
            "dynamodb:Get*",
            "dynamodb:Query",
            "dynamodb:Scan",
            "dynamodb:BatchWrite*",
            "dynamodb:CreateTable",
            "dynamodb:Delete*",
            "dynamodb:Update*",
            "dynamodb:PutItem"
         ],
         "Resource":"arn:aws:dynamodb:us-east-2:857455201587:table/DirtbagReadings"
      }
   ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "save_reading_policy_attachment" {
  role       = aws_iam_role.save_reading_role.name
  policy_arn = aws_iam_policy.save_reading.arn
}

# Render Index Lambda Permissions
resource "aws_iam_role" "render_index_role" {
  name = "dirtbag-render-index-role"

  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
POLICY
}

resource "aws_iam_policy" "render_index" {
  name        = "dirtbag-s3-write"
  description = "Allow DirtBag Pi Render Index Lambda to write to S3"

  policy = <<EOF
{
   "Version":"2012-10-17",
   "Statement":[
      {
         "Effect":"Allow",
         "Action":[
            "s3:PutObject",
            "s3:GetObject",
            "s3:DeleteObject"
         ],
         "Resource":"*"
      },
      {
         "Effect":"Allow",
         "Action":[
            "dynamodb:BatchGet*",
            "dynamodb:DescribeStream",
            "dynamodb:DescribeTable",
            "dynamodb:Get*",
            "dynamodb:Query",
            "dynamodb:Scan",
            "dynamodb:BatchWrite*",
            "dynamodb:CreateTable",
            "dynamodb:Delete*",
            "dynamodb:Update*",
            "dynamodb:PutItem"
         ],
         "Resource":[
            "arn:aws:dynamodb:us-east-2:857455201587:table/DirtbagReadings",
            "arn:aws:dynamodb:us-east-2:857455201587:table/DirtbagReadings/*"
         ]
      }
   ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "render_index_policy_attachment" {
  role       = aws_iam_role.render_index_role.name
  policy_arn = aws_iam_policy.render_index.arn
}

# API Gateway Permissions
resource "aws_iam_role" "api_gateway_cloudwatch" {
  name = "api_gateway_cloudwatch_global"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "apigateway.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "api_gateway_cloudwatch" {
  name = "default"
  role = aws_iam_role.api_gateway_cloudwatch.id

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:DescribeLogGroups",
                "logs:DescribeLogStreams",
                "logs:PutLogEvents",
                "logs:GetLogEvents",
                "logs:FilterLogEvents"
            ],
            "Resource": "*"
        }
    ]
}
EOF
}

# Soil Sensor Client IAM Permissions
resource "aws_iam_user" "dirtbag_client" {
  name = "dirtbag-client"
  path = "/"

  tags = {
    tag-key = "dirtbag-pi"
  }
}

resource "aws_iam_access_key" "dirtbag_client" {
  user = aws_iam_user.dirtbag_client.name
}
resource "aws_iam_user_policy" "client_invoke_api_gateway" {
  name   = "dirtbag-client-invoke-api-gateway"
  user   = aws_iam_user.dirtbag_client.name
  policy = data.aws_iam_policy_document.dirtbag_client.json
}

data "aws_iam_policy_document" "dirtbag_client" {
  statement {

    actions = [
      "execute-api:Invoke"
    ]

    resources = [
      local.save_reading_api_gw_arn
    ]
  }
}