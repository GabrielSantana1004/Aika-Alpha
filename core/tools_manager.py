from tools import datetime_tool, search_tool

# Lista de schemas enviada pra OpenAI descrever quais funções existem
TOOLS_SCHEMA = [
    datetime_tool.TOOL_SCHEMA,
    search_tool.TOOL_SCHEMA,
]

# Mapa nome_da_funcao -> função python real
TOOLS_MAP = {
    "get_current_datetime": datetime_tool.get_current_datetime,
    "web_search": search_tool.web_search,
}


def executar_ferramenta(nome: str, argumentos: dict) -> str:
    """Executa a ferramenta pedida pela IA e retorna o resultado em texto."""
    funcao = TOOLS_MAP.get(nome)
    if funcao is None:
        return f"Ferramenta '{nome}' não existe."

    try:
        return funcao(**argumentos)
    except Exception as e:
        return f"Erro ao executar a ferramenta '{nome}': {e}"
