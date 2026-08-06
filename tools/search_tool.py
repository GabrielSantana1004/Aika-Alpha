import requests

from config import TAVILY_API_KEY
from utils.logger import get_logger

logger = get_logger(__name__)

TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": (
            "Pesquisa na internet (via Tavily). Use quando precisar de "
            "informação atual, notícias, preços, eventos recentes ou qualquer "
            "fato que você não tenha certeza ou que possa ter mudado."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "O termo de busca a ser pesquisado.",
                }
            },
            "required": ["query"],
        },
    },
}


def web_search(query: str, **kwargs) -> str:
    if not TAVILY_API_KEY:
        return "Pesquisa indisponível: TAVILY_API_KEY não configurada no .env."

    try:
        response = requests.post(
            "https://api.tavily.com/search",
            headers={
                "Authorization": f"Bearer {TAVILY_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "query": query,
                "search_depth": "basic",  # "basic" gasta 1 crédito; "advanced" gasta mais
                "include_answer": True,
                "max_results": 5,
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        logger.error(f"Erro ao pesquisar '{query}': {e}")
        return f"Não consegui pesquisar agora ({e})."

    resultados = []

    resposta_direta = data.get("answer")
    if resposta_direta:
        resultados.append(f"Resposta direta: {resposta_direta}")

    for item in data.get("results", [])[:5]:
        titulo = item.get("title", "")
        conteudo = item.get("content", "")
        link = item.get("url", "")
        if titulo or conteudo:
            resultados.append(f"- {titulo}: {conteudo} ({link})")

    if not resultados:
        return f"Nenhum resultado relevante encontrado para '{query}'."

    return "\n".join(resultados)
