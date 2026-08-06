from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(
    title="Syntra Chatbot API",
    description="API do chatbot inteligente para WhatsApp.",
    version="0.1.0"
)

@app.get("/")
def home():
    return {
        "message": "Syntra Chatbot API está funcionando!",
        "database": settings.DATABASE_URL
    }
