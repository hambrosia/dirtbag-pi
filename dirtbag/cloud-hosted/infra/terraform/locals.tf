locals {
  environment = terraform.workspace

  bucket_name = "dirtbag-graph-${split("-", uuid())[0]}"

}

data "aws_region" "current" {}
