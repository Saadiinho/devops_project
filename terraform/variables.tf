variable "aws_region" {
  description = "Region aws"
  type = string
  default = "eu-west-3"
}

variable "instance_type" {
  description = "Type d'instance EC2"
  type = string
  default = "t3.micro"
}

variable "key_name" {
  description = "Nom de la clé SSH"
  type        = string
  default     = "deployer-key"
}

variable "key_public" {
  description = "Public Key"
  type = string
  default = ""
}

variable "my_ip_address" {
  description = "IP Address"
  type = string
  default = "0.0.0.0/0"
}