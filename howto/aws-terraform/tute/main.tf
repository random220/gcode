
provider "aws" {
    region = "us-east-2"
}

resource "aws_key_pair" "omkey" {
  key_name   = "sesame"
  public_key = file("~/.ssh/id_rsa.pub")
}

resource "aws_instance" "gaia" {
    ami = "ami-024e6efaf93d85776"
    instance_type = "t2.micro"
    key_name = aws_key_pair.omkey.key_name

    tags = {
        Name = "gaia1"
    }
}
