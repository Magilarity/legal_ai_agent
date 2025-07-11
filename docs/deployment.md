# Deployment

## Multi-stage Docker

- **builder**: встановлює всі залежності  
- **final**: копіює лише Python-пакети та код  
- **Порти**: 8501 (UI), 8001 (метрики)

```dockerfile
# Stage 1
FROM python:3.13-slim AS builder
...
# Stage 2
FROM python:3.13-slim
...
ENTRYPOINT ["./start.sh"]