output "ec2_public_ips" {
description = "Public IPs for all EC2 instances"
value = [for i in aws_instance.servers : i.public_ip]
}


output "default_vpc_id" {
value = data.aws_vpc.default.id
}


output "used_subnet" {
value = data.aws_subnet_ids.default.ids[0]
}