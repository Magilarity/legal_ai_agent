exit_after_auth = false
pid_file = "vault-agent.pid"

auto_auth {
  method "approle" {
    mount_path = "auth/approle"
    config = {
      role_id_file_path = "/vault/secrets/role_id"
      secret_id_file_path = "/vault/secrets/secret_id"
    }
  }
  sink "file" {
    config = { path = "/vault/secrets/agent_token" }
  }
}

cache {
  use_auto_auth_token = true
}

listener "tcp" {
  address = "127.0.0.1:8200"
  tls_disable = true
}

auto_auth {
  token_path = "/vault/secrets/agent_token"
}

template {
  destination = "/vault/secrets/config.env"
  contents = <<EOF
OPENAI_API_KEY={{ with secret "secret/data/legal-ai-agent" }}{{ .Data.data.OPENAI_API_KEY }}{{ end }}
DATABASE_URL={{ with secret "secret/data/legal-ai-agent" }}{{ .Data.data.DATABASE_URL }}{{ end }}
SLACK_API_URL={{ with secret "secret/data/legal-ai-agent" }}{{ .Data.data.SLACK_API_URL }}{{ end }}
EOF
}