# Magilarity Legal AI Agent

Цей README описує, як розгорнути та використовувати проект **Magilarity Legal AI Agent** — автоматизованого юридичного агента для аналізу документів, генерації шаблонів та моніторингу метрик.

---

## Quickstart

1. **Клонування репозиторію**  
   git clone <repo_url>  
   cd legal_ai_agent

2. **Створення та активація venv**  
   # Windows PowerShell  
   python -m venv venv  
   .\venv\Scripts\Activate.ps1  
   # Windows CMD  
   venv\Scripts\activate.bat  
   # macOS/Linux  
   python3 -m venv venv  
   source venv/bin/activate

3. **Встановлення залежностей**  
   python -m pip install --upgrade pip setuptools wheel  
   pip install -r requirements.txt

4. **Запуск Streamlit**  
   streamlit run interface/streamlit_app.py --server.address=0.0.0.0

---

## Dev Setup

python -m pip install -e .  
pip install -r requirements-dev.txt  
flake8 .  
black --check .  
mypy .  
pytest

---

## Docker & Compose

docker-compose up --build  
.env: POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, SLACK_API_URL

---

## CI/CD

.github/workflows/ci.yml: flake8, black, mypy, pytest, docker build & push  
Secrets: DOCKERHUB_USERNAME, DOCKERHUB_TOKEN, SLACK_API_URL

---

## Terraform

cd terraform  
terraform init  
terraform apply -var="db_username=<USER>" -var="db_password=<PASS>"

---

## Alertmanager

alertmanager --config.file=monitoring/alertmanager.yml

---

## Backup

scripts/backup.sh

---

## Contributing

Fork → branch → PR → CI green → merge

---

## Додаткові команди

- Smoke-test (PowerShell):  
  .\scripts\smoke_test.ps1 -url "http://localhost:8501"

- Документація (MkDocs):  
  mkdocs serve