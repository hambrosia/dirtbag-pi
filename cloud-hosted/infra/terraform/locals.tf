locals {
  environment = terraform.workspace

}

data "aws_region" "current" {}
