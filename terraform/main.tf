provider "aws" {
  region = var.aws_region
}

resource "aws_key_pair" "default" {
  key_name = var.key_name
  public_key = file(var.key_public)
}

resource "aws_security_group" "ssh_http" {
  name = "ssh_http"
  description = "Allow ports 22 and 80"

  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = [var.my_ip_address]
  }

  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "ec2_instance" {
  ami                         = "ami-0ff71843f814379b3" 
  instance_type               = "t3.micro"
  key_name = aws_key_pair.default.key_name
  vpc_security_group_ids = [aws_security_group.ssh_http.id]

  tags = {
    Name = "Backend-Server"
  }
}

output "public_ip" {
  value = aws_instance.ec2_instance.public_ip
}
