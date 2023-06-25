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



# aws help
# aws ec2 help
# % aws ec2 describe-account-attributes
#   You must specify a region. You can also configure your region by running "aws configure".
# % aws configure
# AWS Access Key ID [****************FFN3]: 
# AWS Secret Access Key [****************RaL2]: 
# Default region name [None]: us-east-1
# Default output format [None]: 

# aws ec2 help
# aws ec2 describe-availability-zones
# aws ec2 describe-vpcs
# aws ec2 create-default-vpc
# % aws ec2 describe-vpcs|jq -r '.Vpcs[0].VpcId'
# vpc-0042a28e60b96d1f6

# % aws ec2 delete-vpc --vpc-id vpc-0042a28e60b96d1f6
# An error occurred (DependencyViolation) when calling the DeleteVpc operation: The vpc 'vpc-0042a28e60b96d1f6' has dependencies and cannot be deleted.

# https://docs.aws.amazon.com/vpc/latest/userguide/delete-vpc.html
# To delete a VPC by using the AWS CLI
# 
#     Delete your security group by using the delete-security-group command.
#     aws ec2 delete-security-group --group-id sg-id
#     
#     Delete each network ACL by using the delete-network-acl command.
#     aws ec2 delete-network-acl --network-acl-id acl-id
#     
#     Delete each subnet by using the delete-subnet command.
#     aws ec2 delete-subnet --subnet-id subnet-id
#     
#     Delete each custom route table by using the delete-route-table command.
#     aws ec2 delete-route-table --route-table-id rtb-id
#     
#     Detach your internet gateway from your VPC by using the detach-internet-gateway command.
#     aws ec2 detach-internet-gateway --internet-gateway-id igw-id --vpc-id vpc-id
#     
#     Delete your internet gateway by using the delete-internet-gateway command.
#     aws ec2 delete-internet-gateway --internet-gateway-id igw-id
#     
#     [Dual stack VPC] Delete your egress-only internet gateway by using the delete-egress-only-internet-gateway command.
#     aws ec2 delete-egress-only-internet-gateway --egress-only-internet-gateway-id eigw-id
#     
#     Delete your VPC by using the delete-vpc command.
#     aws ec2 delete-vpc --vpc-id vpc-id
# 
# 

# % aws ec2 describe-key-pairs
# {
#     "KeyPairs": [
#         {
#             "KeyPairId": "key-0c7ca644c7256e71d",
#             "KeyFingerprint": "41:d2:ce:8a:dd:52:12:3b:d6:85:25:9a:b9:98:19:13:ab:46:05:f4",
#             "KeyName": "om",
#             "KeyType": "rsa",
#             "Tags": [],
#             "CreateTime": "2023-06-07T06:31:25.359000+00:00"
#         }
#     ]
# }
# 

# aws ec2 delete-key-pair --key-name om
# aws ec2 create-key-pair --key-name=om --key-type=ed25519

services=("ec2" "s3" "rds" "lambda" "dynamodb")  # Add more service names as needed

for service in "${services[@]}"
do
    echo "Listing $service resources:"
    aws $service describe-*  # Replace * with the appropriate describe command for each service
    echo "------------------------------"
done
