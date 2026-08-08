import asyncio
from ollama import AsyncClient

async def main():
    client = AsyncClient()
    resposta = await client.chat(
        model = 'llama3', 
        messages = [{"role": "user", "content": "Ollama model test"}]
         
    )
        
