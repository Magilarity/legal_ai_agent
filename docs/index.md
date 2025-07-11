# Legal AI Agent

**Legal AI Agent** — це RAG-сервіс для аналізу юридичних документів.

## Архітектура

1. **Streamlit UI** — веб-інтерфейс для користувача  
2. **FastAPI** (за потреби) — REST-API для інтеграцій  
3. **Prometheus** + **Grafana** — моніторинг метрик  
4. **PostgreSQL** — зберігання даних  
5. **RAGEngine** — Retrieval-Augmented Generation пайплайн  
6. **OpenAI / LLMAgent** — генерація відповідей  

> _Детальний опис див. у відповідних розділах._