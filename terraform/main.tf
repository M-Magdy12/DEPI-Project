terraform {
required_version = ">= 1.6.0"


backend "s3" {
bucket = var.backend_bucket
key = var.backend_key
region = var.region
}


required_providers {
aws = {
source = "hashicorp/aws"
version = "~> 5.0"
}
}
}


provider "aws" {
region = var.region
}



data "aws_vpc" "default" {
default = true
}


data "aws_subnet_ids" "default" {
vpc_id = data.aws_vpc.default.id
}


resource "aws_security_group" "ec2_sg" {
name = "default-ec2-sg"
description = "Allow SSH"
vpc_id = data.aws_vpc.default.id


ingress {
description = "SSH"
from_port = 22
to_port = 22
protocol = "tcp"
cidr_blocks = ["0.0.0.0/0"]
}

ingress {
  description = "HTTP"
  from_port   = 80
  to_port     = 80
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}


egress {
from_port = 0
to_port = 0
protocol = "-1"
cidr_blocks = ["0.0.0.0/0"]
}


tags = { Name = "default-ec2-sg" }
}


resource "aws_instance" "servers" {
count = 3
ami = var.ami_id
instance_type = var.instance_type
subnet_id = data.aws_subnet_ids.default.ids[0]
vpc_security_group_ids = [aws_security_group.ec2_sg.id]


tags = {
Name = "default-server-${count.index + 1}"
}
}

resource "aws_security_group" "alb_sg" {
  name        = "alb-sg"
  description = "Allow HTTP"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "alb-sg" }
}

resource "aws_lb" "app_lb" {
  name               = "my-app-lb"
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = data.aws_subnet_ids.default.ids

  tags = { Name = "my-app-lb" }
}


resource "aws_lb_target_group" "tg" {
  name     = "my-target-group"
  port     = 80
  protocol = "HTTP"
  vpc_id   = data.aws_vpc.default.id

  health_check {
    path = "/"
    port = "traffic-port"
  }
}

resource "aws_lb_listener" "http_listener" {
  load_balancer_arn = aws_lb.app_lb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.tg.arn
  }
}


resource "aws_lb_target_group_attachment" "tg_attachment" {
  count            = length(aws_instance.servers)
  target_group_arn = aws_lb_target_group.tg.arn
  target_id        = aws_instance.servers[count.index].id
  port             = 80
}
