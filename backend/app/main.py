from fastapi import FastAPI
from app.api.routes.chat import router as chat_router
from app.api.routes.webhook import router as webhook_router
from app.core.config import settings

app = FastAPI(
    title="Syntra Chatbot API",
    description="API do chatbot inteligente para WhatsApp.",
    version="0.1.0"
)
app.include_router(chat_router, prefix="/api/v1")
app.include_router(webhook_router, prefix = "/api/v1")

@app.get("/")
def home():
    return {
        "message": "Syntra Chatbot API está funcionando!",
        "database": settings.DATABASE_URL
    }

