import httpx
import ollama
from ollama import AsyncClient

from app.core.config import settings


class OllamaIndisponivelError(Exception):
    """O serviço Ollama não respondeu corretamente."""


async def gerar_resposta(
    prompt: str,
    historico: list[dict[str, str]] | None = None,
) -> str:
    client = AsyncClient(
        host=settings.OLLAMA_HOST,
        timeout=settings.OLLAMA_TIMEOUT_SECONDS,
    )

    mensagens = [
        {
            "role": "system",
            "content": (
                "Você é um assistente de IA chamado Syntra, "
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

    try:
        resposta = await client.chat(
            model=settings.OLLAMA_MODEL,
            messages=mensagens,
        )
    except (httpx.HTTPError, ollama.ResponseError) as exc:
        raise OllamaIndisponivelError(
            "Não foi possível obter resposta do Ollama."
        ) from exc

    return resposta["message"]["content"]