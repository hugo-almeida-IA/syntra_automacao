from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.api.routes.chat import router as chat_router
from app.api.routes.webhook import router as webhook_router
from app.core.config import settings
from app.database.session import SessionLocal


app = FastAPI(
    title=settings.APP_NAME,
    description="API do chatbot inteligente para WhatsApp.",
    version="0.1.0",
)

app.include_router(chat_router, prefix="/api/v1")
app.include_router(webhook_router, prefix="/api/v1")


@app.get("/", tags=["Sistema"])
def home():
    return {
        "message": "Syntra Chatbot API está funcionando!",
        "environment": settings.APP_ENV,
    }


@app.get("/health", tags=["Sistema"])
def health():
    try:
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=503,
            detail="Banco de dados indisponível.",
        ) from exc

    return {
        "status": "ok",
        "database": "ok",
        "environment": settings.APP_ENV,
    }