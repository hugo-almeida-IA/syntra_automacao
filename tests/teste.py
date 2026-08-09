import asyncio 
from backend.app.ai.ollama_main import gerar_resposta
async def main():
    prompt = "Qual a capital do Brasil?"
    resposta = await gerar_resposta(prompt)
    print(resposta)

asyncio.run(main())