# variables.tf
# ── AWS ───────────────────────────────────────
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "aws_profile" {
  description = "AWS CLI profile to use for credentials"
  type        = string
  default     = "default"
}

# ── EC2 / Application server ───────────────────
variable "instance_type" {
  description = "EC2 instance type for the application server"
  type        = string
  default     = "t3.micro"
}

variable "app_port" {
  description = "Port on which the Streamlit app will run"
  type        = number
  default     = 8501
}

# ── PostgreSQL ─────────────────────────────────
variable "db_name" {
  description = "Name of the PostgreSQL database"
  type        = string
  default     = "appdb"
}

variable "db_username" {
  description = "Username for the PostgreSQL database"
  type        = string
}

variable "db_password" {
  description = "Password for the PostgreSQL database"
  type        = string
  sensitive   = true
}

variable "db_port" {
  description = "Port on which PostgreSQL listens"
  type        = number
  default     = 5432
}