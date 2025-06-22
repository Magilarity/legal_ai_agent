output "db_endpoint" {
  description = "Connection endpoint for the database"
  value       = aws_db_instance.postgres.address
}
