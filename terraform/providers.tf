terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region  = var.aws_region
  # Якщо ви використовуєте AWS CLI profile, розкоментуйте:
  # profile = var.aws_profile
}