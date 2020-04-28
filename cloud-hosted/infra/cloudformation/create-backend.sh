#!/bin/bash

aws --region us-east-2 cloudformation create-stack --stack-name dirtbag-terraform-s3-backend --template-body file://s3_backend.yaml
