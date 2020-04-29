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

resource "aws_iam_policy" "save_reading_policy" {
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
         "Resource":"arn:aws:dynamodb:*:*:table/DirtbagReadings"
      }
   ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "test-attach" {
  role       = "${aws_iam_role.save_reading_role.name}"
  policy_arn = "${aws_iam_policy.save_reading_policy.arn}"
}