variable "region" {
description = "AWS Region"
type = string
default = "eu-north-1"
}


variable "ami_id" {
description = "EC2 AMI ID"
type = string
}


variable "instance_type" {
description = "EC2 instance type"
type = string
default = "t3.small"
}


variable "backend_bucket" {
description = "S3 bucket for Terraform state"
type = string
}


variable "backend_key" {
description = "State file path inside bucket"
type = string
}