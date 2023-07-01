# https://adamtheautomator.com/terraform-vpc/
#
# VPC
#
# Subnet
# Gateway
# Routing table
# Routing table association

# -----------------------------------------------------------------------------------------------
resource "aws_vpc" "see-vpc" {         # Creating VPC here
  cidr_block       = var.main_vpc_cidr # Defining the CIDR block use 10.0.0.0/24 for demo
  instance_tenancy = "default"
}
output "defsg" {
  value       = aws_vpc.see-vpc.default_security_group_id
  description = "hi"
}

# https://spacelift.io/blog/terraform-security-group
# add a new inbound rule to the default security group
resource "aws_security_group_rule" "allow_all" {
  type              = "ingress"
  description       = "allow all"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_vpc.see-vpc.default_security_group_id
}
# -----------------------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------------------
resource "aws_subnet" "see-sub-pub" { # Creating Public Subnets
  vpc_id                  = aws_vpc.see-vpc.id
  cidr_block              = var.public_subnets # CIDR block of public subnets
  map_public_ip_on_launch = true
}
resource "aws_internet_gateway" "see-igw" { # Creating Internet Gateway
  vpc_id = aws_vpc.see-vpc.id               # vpc_id will be generated after we create VPC
}
resource "aws_route_table" "see-pub-rt" { # Creating RT for Public Subnet
  vpc_id = aws_vpc.see-vpc.id
  route {
    cidr_block = "0.0.0.0/0" # Traffic from Public Subnet reaches Internet via Internet Gateway
    gateway_id = aws_internet_gateway.see-igw.id
  }
}
resource "aws_route_table_association" "see-rtassoc-pub" {
  subnet_id      = aws_subnet.see-sub-pub.id
  route_table_id = aws_route_table.see-pub-rt.id
}
# -----------------------------------------------------------------------------------------------

/*
# -----------------------------------------------------------------------------------------------
resource "aws_subnet" "privatesubnets" {
  vpc_id     = aws_vpc.Main.id
  cidr_block = var.private_subnets # CIDR block of private subnets
}
resource "aws_eip" "nateIP" {
  vpc = true
}
resource "aws_nat_gateway" "NATgw" {
  allocation_id = aws_eip.nateIP.id
  subnet_id     = aws_subnet.publicsubnets.id
}
resource "aws_route_table" "PrivateRT" { # Creating RT for Private Subnet
  vpc_id = aws_vpc.Main.id
  route {
    cidr_block     = "0.0.0.0/0" # Traffic from Private Subnet reaches Internet via NAT Gateway
    nat_gateway_id = aws_nat_gateway.NATgw.id
  }
}
resource "aws_route_table_association" "PrivateRTassociation" {
  subnet_id      = aws_subnet.privatesubnets.id
  route_table_id = aws_route_table.PrivateRT.id
}
# -----------------------------------------------------------------------------------------------
*/

