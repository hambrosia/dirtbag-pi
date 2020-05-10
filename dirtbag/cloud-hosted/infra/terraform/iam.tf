# Save Reading Lambda Permissions
resource "aws_iam_role" "save_reading" {
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
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents"
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
         "Resource":"arn:aws:dynamodb:us-east-2:857455201587:table/DirtbagReadings"
      }
   ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "save_reading" {
  role       = aws_iam_role.save_reading.name
  policy_arn = aws_iam_policy.save_reading.arn
}

# Render Index Lambda Permissions
resource "aws_iam_role" "render_index" {
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
  name        = "dirtbag-render-index"
  description = "Allow DirtBag Pi Render Index Lambda to write to S3"

  policy = <<EOF
{
   "Version":"2012-10-17",
   "Statement":[
      {
         "Effect":"Allow",
         "Action":[
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents"
         ],
         "Resource":"*"
      },
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

resource "aws_iam_role_policy_attachment" "render_index" {
  role       = aws_iam_role.render_index.name
  policy_arn = aws_iam_policy.render_index.arn
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
resource "aws_iam_user_policy" "client_invoke_lambda" {
  name   = "dirtbag-client-invoke-lambda"
  user   = aws_iam_user.dirtbag_client.name
  policy = data.aws_iam_policy_document.dirtbag_client.json
}

data "aws_iam_policy_document" "dirtbag_client" {
  statement {

    actions = [
      "lambda:InvokeFunction"
    ]

    resources = [
      aws_lambda_function.save_reading.arn
    ]
  }
}


data "aws_iam_policy_document" "graph_bucket_public" {
  statement {
    principals {
      identifiers = ["*"]
      type = "AWS"
    }
    	actions = [
			"s3:GetObject"
    	]

    	resources = [
    		aws_s3_bucket.index.arn,
    		"${aws_s3_bucket.index.arn}/*"
    	]
  }
}