
provider "aws" {
    region = "us-east-2"
}

resource "aws_key_pair" "omkey_sesame" {
  key_name   = "sesame"
  public_key = file("~/.ssh/id_rsa-sesame.pub")
}

variable "http_port" {
    description = "HTTP port"
    type = number
    default = 8080
}
variable "ssh_port" {
    description = "SSH port"
    type = number
    default = 22
}

resource "aws_security_group" "ports_http_ssh" {
    name = "sg_ports_http_ssh"
    ingress {
        from_port = var.http_port
        to_port = var.http_port
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
    ingress {
        from_port = var.ssh_port
        to_port = var.ssh_port
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

resource "aws_instance" "gaia" {
    ami = "ami-024e6efaf93d85776"
    instance_type = "t2.micro"
    vpc_security_group_ids = [aws_security_group.ports_http_ssh.id]
    key_name = aws_key_pair.omkey_sesame.key_name

    user_data = <<-EOF
                #!/bin/bash
                echo "Hello, World" >index.html
                nohup busybox httpd -f -p 8080 &
                EOF
    tags = {
        Name = "gaia"
    }

}

output "pubdns" {
    value = aws_instance.gaia.public_dns
    description = "Public DNS name of instance"
}
