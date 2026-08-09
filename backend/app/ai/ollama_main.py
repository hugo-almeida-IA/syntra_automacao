import asyncio, ollama
from ollama import AsyncClient

async def gerar_resposta(prompt: str) -> str:
    client = AsyncClient()
    resposta = await client.chat(
        model = 'llama3', 
        messages = [
            {"role": "system", "content": 'Você é um asistente de IA chamado Syntra, que responde a cada pergunta de forma clara e objetiva, sem rodeios. Você não deve inventar respostas, apenas responder com base em fatos. Por se tratar de uma IA no Brasil, você deve responder sempre em português, há não ser que seja pedido para a resposta ser em outro idioma.'},
            {"role": "user", "content": prompt}
            ]
         
    )
    return resposta['message']['content']
