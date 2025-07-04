# Legal AI Agent “Маджіларіті”

Цей README описує, як запускати тести, налаштувати CI/CD, інфраструктуру Terraform, Alertmanager і скрипти резервного копіювання.

---

## Запуск тестів

1. **Створіть і активуйте віртуальне середовище**  
   - Windows (PowerShell):  
     ```powershell
     python -m venv venv
     venv\Scripts\Activate.ps1
     ```  
   - macOS/Linux:  
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```  
2. **Встановіть залежності**  
   ```bash
   pip install -r requirements.txt
   ```  
3. **Запустіть тести**  
   ```bash
   python -m pytest -q
   ```  

---

## CI/CD (GitHub Actions)

У каталозі `.github/workflows/ci.yml` визначено такий pipeline:

- **on**: `push` та `pull_request` до гілки `main`
- **jobs.lint_and_test**:
  - Лінтинг: `flake8 .`
  - Перевірка форматування: `black --check .`
  - Типізація: `mypy app`
  - Запуск тестів: `pytest -q`
- **jobs.build_and_push** (після успішного проходження lint_and_test):
  - Авторизація у Docker Hub через secret’и `DOCKERHUB_USERNAME` та `DOCKERHUB_TOKEN`
  - Збірка та push образу  
    ```bash
    IMAGE_NAME=${{ secrets.DOCKERHUB_USERNAME }}/legal_ai_agent:latest
    docker build -t $IMAGE_NAME .
    docker push $IMAGE_NAME
    ```

### Налаштування CI/CD

1. Додайте в GitHub репозиторій Secrets:
   - `DOCKERHUB_USERNAME`
   - `DOCKERHUB_TOKEN`
2. Перевірте, що файл `.github/workflows/ci.yml` присутній.

---

## Terraform

У папці `terraform/` знаходяться:
- `main.tf` – налаштування AWS RDS PostgreSQL
- `variables.tf` – змінні `db_username`, `db_password`
- `outputs.tf` – вивід `db_endpoint`

### Команди

```bash
cd terraform
terraform init
terraform apply -var="db_username=<USERNAME>" -var="db_password=<PASSWORD>"
```

---

## Alertmanager

Конфігурація у `monitoring/alertmanager.yml`. Щоб запустити Alertmanager:

```bash
alertmanager --config.file=monitoring/alertmanager.yml
```

Замініть у файлі `{{ slack_api_url }}` на ваш Slack Webhook (через GitHub Secret `SLACK_API_URL`).

---

## Резервне копіювання

Скрипт `scripts/backup.sh` створює dump PostgreSQL у `/backups`:

```bash
# Переконайтеся, що змінна середовища DATABASE_URL встановлена
./scripts/backup.sh
```

---

Перевірте, що усі файли (CI, Terraform, Alertmanager, скрипт бекапу) розташовані у відповідних папках, а середовища налаштовані відповідно до опису вище.
#   l e g a l _ a i _ a g e n t  
 