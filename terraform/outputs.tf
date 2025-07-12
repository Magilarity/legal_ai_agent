output "db_endpoint" {
  description = "Postgres container endpoint (address:port)"
  value       = "${docker_container.postgres.name}:${var.db_port}"
}

output "app_url" {
  description = "URL of the deployed Streamlit app"
  value       = "http://localhost:${var.app_port}"
}

output "metrics_url" {
  description = "URL of the app metrics endpoint"
  value       = "http://localhost:8002/metrics"
}

output "grafana_url" {
  description = "URL of Grafana dashboard"
  value       = "http://localhost:${var.grafana_port}"
}

output "grafana_credentials" {
  description = "Grafana login credentials"
  value = {
    username = var.grafana_admin_user
    password = var.grafana_admin_password
  }
  sensitive = true
}

output "prometheus_url" {
  description = "URL of Prometheus UI"
  value       = "http://localhost:${var.prometheus_port}"
}

output "database_connection" {
  description = "Database connection string"
  value       = "postgres://${var.db_username}:${var.db_password}@localhost:${var.db_port}/${var.db_name}"
  sensitive   = true
}
