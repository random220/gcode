#!/bin/bash

# Setting up access key
#   1. Generate at https://us-east-1.console.aws.amazon.com/iamv2/home?region=us-east-1#/security_credentials
#   2. Store as
#        ~/.ssh/aws/key-id
#        ~/.ssh/aws/key-secret
#   3. aws configure
#   3. % aws configure
#        AWS Access Key ID [None]: xxx
#        AWS Secret Access Key [None]: yyy
#        Default region name [None]:
#        Default output format [None]:
#
#      That created ~/.aws/credentials
#      [default]
#      aws_access_key_id = xxx
#      aws_secret_access_key = yyy



services=("ec2" "s3" "rds" "lambda" "dynamodb")  # Add more service names as needed

for service in "${services[@]}"
do
    echo "Listing $service resources:"
    aws $service describe-*  # Replace * with the appropriate describe command for each service
    echo "------------------------------"
done
