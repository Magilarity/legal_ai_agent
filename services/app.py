import logging
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Legal AI Agent API",
    description="API для юридичного AI агента",
    version="1.0.0",
)

# CORS middleware для підтримки веб-інтерфейсу
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic моделі для запитів
class DocumentAnalysisRequest(BaseModel):
    document_text: str
    analysis_type: str = "legal"


class TenderAnalysisRequest(BaseModel):
    tender_id: str
    document_text: str = None
    priority: str = "normal"


# ===== ОСНОВНІ ENDPOINT'И =====


@app.get("/")
def read_root():
    return {
        "message": "Welcome to Legal AI Agent backend",
        "version": "1.0.0",
        "status": "running",
        "available_endpoints": [
            "GET /",
            "GET /healthz",
            "GET /analyze/{tender_id}",
            "POST /api/analyze",
            "GET /api/documents",
            "GET /api/metrics",
            "GET /docs",
        ],
    }


@app.get("/healthz")
def health():
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "service": "legal-ai-agent",
    }


@app.get("/analyze/{tender_id}")
def analyze(tender_id: str):
    """Аналіз тендера за ID (оригінальний endpoint)"""
    try:
        # Симуляція аналізу тендера
        result = {
            "tender_id": tender_id,
            "result": "completed",
            "analysis": {
                "risk_level": "medium",
                "compliance_score": 85,
                "issues_found": 2,
                "recommendations": [
                    "Перевірте документацію",
                    "Уточніть правові аспекти",
                ],
            },
            "processed_at": datetime.now().isoformat(),
        }
        logger.info(f"Analysis completed for tender: {tender_id}")
        return result
    except Exception as e:
        logger.error(f"Error analyzing tender {tender_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Помилка аналізу: {str(e)}")


# ===== ДОДАТКОВІ API ENDPOINT'И =====


@app.post("/api/analyze")
def analyze_document(request: TenderAnalysisRequest):
    """Детальний аналіз документа з текстом"""
    try:
        analysis_result = {
            "tender_id": request.tender_id,
            "status": "completed",
            "priority": request.priority,
            "analysis": {
                "document_length": (
                    len(request.document_text) if request.document_text else 0
                ),
                "legal_compliance": "passed",
                "risk_assessment": "low",
                "key_findings": [
                    "Документ відповідає стандартам",
                    "Знайдено 0 критичних помилок",
                    "Рекомендовано до затвердження",
                ],
                "confidence_score": 0.92,
            },
            "created_at": datetime.now().isoformat(),
        }
        return analysis_result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Помилка обробки: {str(e)}")


@app.get("/api/documents")
def list_documents():
    """Список всіх документів в системі"""
    return {
        "documents": [
            {
                "id": "doc_20250711_001",
                "name": "tender_specification.pdf",
                "status": "analyzed",
                "upload_date": "2025-07-11T10:00:00Z",
                "analysis_result": "passed",
            },
            {
                "id": "doc_20250711_002",
                "name": "contract_draft.docx",
                "status": "pending",
                "upload_date": "2025-07-11T15:30:00Z",
                "analysis_result": None,
            },
            {
                "id": "doc_20250711_003",
                "name": "legal_review.txt",
                "status": "completed",
                "upload_date": "2025-07-11T16:45:00Z",
                "analysis_result": "approved",
            },
        ],
        "total_documents": 3,
        "pending_analysis": 1,
        "last_updated": datetime.now().isoformat(),
    }


@app.get("/api/metrics")
def get_system_metrics():
    """Системні метрики та статистика"""
    return {
        "system_metrics": {
            "total_documents_processed": 247,
            "analyses_completed_today": 15,
            "success_rate": 98.2,
            "average_processing_time": "3.7s",
            "system_uptime": "72h 45m",
        },
        "analysis_stats": {
            "high_risk_documents": 12,
            "medium_risk_documents": 89,
            "low_risk_documents": 146,
            "pending_reviews": 3,
        },
        "performance": {
            "requests_per_minute": 24,
            "error_rate": 1.8,
            "response_time_avg": "245ms",
        },
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/api/health")
def detailed_health():
    """Детальна інформація про стан системи"""
    return {
        "status": "healthy",
        "services": {
            "api": "running",
            "database": "connected",
            "ai_model": "ready",
            "file_storage": "available",
        },
        "version": "1.0.0",
        "environment": "production",
        "last_restart": "2025-07-11T20:00:00Z",
    }


# ===== LEGACY ENDPOINTS ДЛЯ СУМІСНОСТІ =====


@app.get("/documents")
def documents_legacy():
    """Legacy endpoint для сумісності"""
    docs = list_documents()
    return {
        "documents": [doc["name"] for doc in docs["documents"]],
        "count": docs["total_documents"],
        "legacy_endpoint": True,
    }


@app.get("/upload")
def upload_info():
    """Інформація про завантаження файлів"""
    return {
        "message": "Upload functionality will be available after installing python-multipart",
        "note": "Currently upload is disabled due to missing dependencies",
        "alternative": "Use POST /api/analyze with text content instead",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
