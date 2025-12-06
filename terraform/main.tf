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