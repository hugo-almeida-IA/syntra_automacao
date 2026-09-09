import ollama
from ollama import AsyncClient


async def gerar_resposta(
    prompt: str,
    historico: list[dict[str, str]] | None = None,
) -> str:
    client = AsyncClient()

    mensagens = [
        {
            "role": "system",
            "content": (
                "Você é um asistente de IA chamado Syntra, "
                "que responde a cada pergunta de forma clara e objetiva, "
                "sem rodeios. Você não deve inventar respostas, apenas "
                "responder com base em fatos. Por se tratar de uma IA no "
                "Brasil, você deve responder sempre em português, a não ser "
                "que seja pedido para a resposta ser em outro idioma."
            ),
        }
    ]

    if historico:
        mensagens.extend(historico)

    mensagens.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    resposta = await client.chat(
        model="llama3",
        messages=mensagens,
    )

    return resposta["message"]["content"]