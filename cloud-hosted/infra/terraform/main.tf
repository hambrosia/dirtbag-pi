provider "aws" {
  region = "us-east-2"
}

terraform {
  backend "s3" {
    bucket = "dirtbag-terraform-state"
    key    = "terraform/dirtbag/terraform.tfstate"
    region = "us-east-2"
  }
  required_version = "0.12.24"
}
