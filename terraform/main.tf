terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

# --- Docker volume for Postgres data ---
resource "docker_volume" "db_data" {
  name = "db_data"
}

# --- Docker volume for Grafana data ---
resource "docker_volume" "grafana_data" {
  name = "grafana_data"
}

# --- Postgres image and container ---
resource "docker_image" "postgres" {
  name = "postgres:15"
}

resource "docker_container" "postgres" {
  name    = "legal_ai_agent_db"
  image   = docker_image.postgres.name
  restart = "unless-stopped"

  mounts {
    source = docker_volume.db_data.name
    target = "/var/lib/postgresql/data"
    type   = "volume"
  }

  ports {
    internal = 5432
    external = 5432
  }

  env = [
    "POSTGRES_USER=${var.db_username}",
    "POSTGRES_PASSWORD=${var.db_password}",
    "POSTGRES_DB=${var.db_name}"
  ]

  healthcheck {
    test     = ["CMD", "pg_isready", "-U", var.db_username]
    interval = "30s"
    timeout  = "10s"
    retries  = 5
  }
}

# --- Streamlit app image and container ---
resource "docker_image" "app" {
  name         = "legal_ai_agent-app:latest"
  keep_locally = true
}

resource "docker_container" "app" {
  name       = "legal_ai_agent"
  image      = docker_image.app.name
  restart    = "unless-stopped"
  depends_on = [docker_container.postgres]

  env = [
    "DATABASE_URL=postgres://${var.db_username}:${var.db_password}@${docker_container.postgres.name}:${var.db_port}/${var.db_name}"
  ]

  ports {
    internal = 8501
    external = 8501
  }
  ports {
    internal = 8002
    external = 8002
  }
  ports {
    internal = 8000
    external = 8000
  }

  healthcheck {
    test     = ["CMD", "curl", "-f", "http://localhost:8002/metrics"]
    interval = "30s"
    timeout  = "5s"
    retries  = 3
  }
}

# --- Prometheus image and container ---
resource "docker_image" "prometheus" {
  name = "prom/prometheus:latest"
}

resource "docker_container" "prometheus" {
  name       = "prometheus"
  image      = docker_image.prometheus.name
  restart    = "unless-stopped"
  depends_on = [docker_container.app]

  mounts {
    source    = abspath("${path.module}/../monitoring/prometheus.yml")
    target    = "/etc/prometheus/prometheus.yml"
    type      = "bind"
    read_only = true
  }
  mounts {
    source    = abspath("${path.module}/../monitoring/alerts.rules.yml")
    target    = "/etc/prometheus/alerts.rules.yml"
    type      = "bind"
    read_only = true
  }

  ports {
    internal = 9090
    external = 9090
  }

  healthcheck {
    test     = ["CMD", "curl", "-f", "http://localhost:9090/metrics"]
    interval = "30s"
    timeout  = "5s"
    retries  = 3
  }
}

# --- Grafana image and container ---
resource "docker_image" "grafana" {
  name = "grafana/grafana:latest"
}

resource "docker_container" "grafana" {
  name       = "grafana"
  image      = docker_image.grafana.name
  restart    = "unless-stopped"
  depends_on = [docker_container.prometheus]

  mounts {
    source = docker_volume.grafana_data.name
    target = "/var/lib/grafana"
    type   = "volume"
  }
  mounts {
    source    = abspath("${path.module}/../monitoring/grafana/provisioning")
    target    = "/etc/grafana/provisioning"
    type      = "bind"
    read_only = true
  }

  ports {
    internal = 3000
    external = 3000
  }

  env = [
    "GF_SECURITY_ADMIN_PASSWORD=${var.grafana_admin_password}",
    "GF_USERS_ALLOW_SIGN_UP=false"
  ]

  healthcheck {
    test     = ["CMD", "curl", "-f", "http://localhost:3000"]
    interval = "30s"
    timeout  = "5s"
    retries  = 3
  }
}
