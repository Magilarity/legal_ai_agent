# outputs.tf
output "db_endpoint" {
  description = "Postgres endpoint (address:port)"
  value       = "${aws_db_instance.postgres.address}:${var.db_port}"
}

output "app_url" {
  description = "URL of the deployed Streamlit app"
  value       = "http://${aws_db_instance.postgres.address}:${var.app_port}"
}

output "grafana_url" {
  description = "URL of Grafana dashboard"
  value       = "http://${aws_db_instance.postgres.address}:3000"
}

output "prometheus_url" {
  description = "URL of Prometheus UI"
  value       = "http://${aws_db_instance.postgres.address}:9090"
}