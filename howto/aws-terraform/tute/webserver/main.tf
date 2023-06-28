
provider "aws" {
    region = "us-east-2"
}

resource "aws_key_pair" "omkey_sesame" {
  key_name   = "sesame"
  public_key = file("~/.ssh/id_rsa-sesame.pub")
}

resource "aws_security_group" "port_8080" {
    name = "name_portia_8080"
    ingress {
        from_port = 8080
        to_port = 8080
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
    ingress {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

resource "aws_instance" "gaia" {
    ami = "ami-024e6efaf93d85776"
    instance_type = "t2.micro"
    vpc_security_group_ids = [aws_security_group.port_8080.id]
    key_name = aws_key_pair.omkey_sesame.key_name

    user_data = <<-EOF
                #!/bin/bash
                echo "Hello, World" >index.html
                nohup busybox httpd -f -p 8080 &
                EOF
    tags = {
        Name = "gaia1"
    }
}

