locals {
  environment = terraform.workspace
  graph_prefix = "${var.instantiation_name}-bucket-"
  dynamo_table_name = "${var.instantiation_name}-dyanmo-table"
}

data "aws_region" "current" {}
