// variables.tf - Змінні для Legal AI Agent

# === Database Variables ===
variable "db_image" {
  description = "Docker image for PostgreSQL"
  type        = string
  default     = "postgres:15"
}

variable "db_container_name" {
  description = "Container name for PostgreSQL"
  type        = string
  default     = "legal_ai_agent_db"
}

variable "db_name" {
  description = "Name of the PostgreSQL database"
  type        = string
  default     = "legal_ai_agent_db"  # Змінено з "appdb" на більш описову назву
}

variable "db_username" {
  description = "Postgres user"
  type        = string
  default     = "legal_agent"  # Змінено з "user" на більш описову назву
}

variable "db_password" {
  description = "Postgres password"
  type        = string
  sensitive   = true
  # ВИДАЛЕНО default - пароль має бути заданий явно для безпеки
  validation {
    condition     = length(var.db_password) >= 8
    error_message = "Database password must be at least 8 characters long."
  }
}

variable "db_port" {
  description = "Port on which Postgres is exposed"
  type        = number
  default     = 5432
}

# === Application Variables ===
variable "app_image" {
  description = "Docker image for the Streamlit app"
  type        = string
  default     = "legal_ai_agent-app:latest"
}

variable "app_container_name" {
  description = "Container name for the Streamlit app"
  type        = string
  default     = "legal_ai_agent"
}

variable "app_port" {
  description = "Port on which the Streamlit app UI is exposed"
  type        = number
  default     = 8501
}

variable "metrics_port" {
  description = "Port on which the app exposes Prometheus metrics"
  type        = number
  default     = 8002
}

# === API Keys (Sensitive) ===
variable "openai_api_key" {
  description = "OpenAI API key"
  type        = string
  sensitive   = true
  # Без default - має бути заданий явно
}

variable "slack_api_url" {
  description = "Slack webhook URL"
  type        = string
  sensitive   = true  # Додано sensitive = true для безпеки
  default     = ""    # Опціональний параметр
}

# === Monitoring Variables ===
variable "prometheus_image" {
  description = "Docker image for Prometheus"
  type        = string
  default     = "prom/prometheus:latest"
}

variable "prometheus_container_name" {
  description = "Container name for Prometheus"
  type        = string
  default     = "prometheus"
}

variable "prometheus_port" {
  description = "Port on which Prometheus UI is exposed"
  type        = number
  default     = 9090
}

variable "grafana_image" {
  description = "Docker image for Grafana"
  type        = string
  default     = "grafana/grafana:latest"
}

variable "grafana_container_name" {
  description = "Container name for Grafana"
  type        = string
  default     = "grafana"
}

variable "grafana_port" {
  description = "Port on which Grafana UI is exposed"
  type        = number
  default     = 3000
}

variable "grafana_admin_user" {
  description = "Grafana admin user"
  type        = string
  default     = "admin"
}

variable "grafana_admin_password" {
  description = "Grafana admin password"
  type        = string
  sensitive   = true
  # ВИДАЛЕНО default - пароль має бути заданий явно для безпеки
  validation {
    condition     = length(var.grafana_admin_password) >= 8
    error_message = "Grafana admin password must be at least 8 characters long."
  }
}

# === Environment Variables ===
variable "environment" {
  description = "Environment (development, staging, production)"
  type        = string
  default     = "development"
  validation {
    condition     = contains(["development", "staging", "production"], var.environment)
    error_message = "Environment must be one of: development, staging, production."
  }
}