# Save Reading Lambda Permissions
resource "aws_iam_role" "save_reading" {
  name = "${var.instantiation_name}-save-reading-role"

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
  name        = "${var.instantiation_name}-dynamo-write"
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
         "Resource":"${aws_dynamodb_table.dirtbag-dynamodb-table.arn}"
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
  name = "${var.instantiation_name}-render-index-role"

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
  name        = "${var.instantiation_name}-render-index"
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
            "s3:GetObject"
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
            "dynamodb:Scan"
         ],
         "Resource":[
            "${aws_dynamodb_table.dirtbag-dynamodb-table.arn}",
            "${aws_dynamodb_table.dirtbag-dynamodb-table.arn}/*"
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
  name = "${var.instantiation_name}-client"
  path = "/"

  tags = {
    tag-key = "dirtbag-pi"
  }
}

resource "aws_iam_access_key" "dirtbag_client" {
  user = aws_iam_user.dirtbag_client.name
}

resource "aws_iam_user_policy" "client_invoke_lambda" {
  name   = "${var.instantiation_name}-client-invoke-lambda"
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

# Client can read from S3 permissions
resource "aws_iam_role" "dirtbag_web_ui_authenticated" {
  name = "${var.instantiation_name}-web-ui-authenticated"
  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Federated": "cognito-identity.amazonaws.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "cognito-identity.amazonaws.com:aud": "${aws_cognito_identity_pool.dirtbag_ui_id_pool.id}"
        },
        "ForAnyValue:StringLike": {
          "cognito-identity.amazonaws.com:amr": "authenticated"
        }
      }
    }
  ]
}
POLICY
}

resource "aws_iam_policy" "dirtbag_web_ui_authenticated" {
  name        = "${var.instantiation_name}-web-ui-authenticated"
  description = "Allow DirtBag Pi UI to do authenticated stuff"

  policy = <<POLICY
{
	"Version": "2012-10-17",
	"Statement": [{
		"Effect": "Allow",
		"Action": [
			"s3:GetObject"
		],
		"Resource": "${aws_s3_bucket.index.arn}/*"
	}]
}
POLICY
}

resource "aws_iam_role_policy_attachment" "dirtbag_web_ui_authenticated" {
  role       = aws_iam_role.dirtbag_web_ui_authenticated.name
  policy_arn = aws_iam_policy.dirtbag_web_ui_authenticated.arn
}
