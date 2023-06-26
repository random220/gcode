
provider "aws" {
    region = "us-east-2"
}

resource "aws_instance" "gaia" {
    ami = "ami-024e6efaf93d85776"
    instance_type = "t2.micro"

    tags = {
        Name = "gaia1"
    }
}
