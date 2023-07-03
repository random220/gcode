resource "aws_key_pair" "see-key" {
  key_name   = "see-key"
  public_key = file("~/.ssh/id_rsa-sesame.pub")
}