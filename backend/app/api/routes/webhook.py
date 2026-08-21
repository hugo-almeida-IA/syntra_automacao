from fastapi import APIRouter

router = APIRouter()
@router.post("/evolution")
async def route_webhook(payload: dict):
    print("Recebido webhook:", payload)

    return {"status": "Webhook recebido com sucesso!"}
