resource "aws_launch_configuration" "see-launch-config" {
  image_id      = "ami-024e6efaf93d85776"
  instance_type = "t2.micro"
  #security_groups = [aws_vpc.see-vpc.default_security_group_id]
  security_groups = ["sg-0851fa3df0ef1335e"]
  user_data       = <<-EOF
                #!/bin/bash
                echo "Hello, World" > index.html
                nohup busybox httpd -f -p ${var.server_port} &
                EOF
}


resource "aws_autoscaling_group" "see-asg-example" {
  launch_configuration = aws_launch_configuration.see-launch-config.name
  availability_zones   = ["us-east-2a"]
  min_size             = 2
  max_size             = 10
  tag {
    key                 = "Name"
    value               = "see-asg-example"
    propagate_at_launch = true
  }
}