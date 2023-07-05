
resource "aws_instance" "gaia" {
  ami                         = "ami-024e6efaf93d85776"
  instance_type               = "t2.micro"
  subnet_id                   = aws_subnet.see-sub-pub.id
  associate_public_ip_address = "true"
  key_name                    = aws_key_pair.see-key.key_name
  vpc_security_group_ids      = [aws_security_group.see-sg-allow-all.id]
  #vpc_security_group_ids     = [aws_vpc.see-vpc.default_security_group_id]

  tags = {
    Name = "gaia"
  }
}
/*
output "pubdns" {
    value = aws_instance.gaia.public_dns
    description = "Public DNS name of instance"
}
*/