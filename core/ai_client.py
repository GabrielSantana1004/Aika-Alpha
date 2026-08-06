import json

from openai import OpenAI

from config import OPENAI_API_KEY, OPENAI_MODEL
from core.personality import SYSTEM_PROMPT
from core.tools_manager import TOOLS_SCHEMA, executar_ferramenta
from utils.logger import get_logger

logger = get_logger(__name__)

_client = OpenAI(api_key=OPENAI_API_KEY)

MAX_TOOL_ITERATIONS = 5  # trava de segurança pra não entrar em loop infinito de function calls


def gerar_resposta(historico: list[dict]) -> str:
    """
    Recebe o histórico de mensagens (user/assistant, sem o system prompt) e
    devolve a resposta final da IA já em texto, resolvendo por baixo dos panos
    qualquer chamada de ferramenta que for necessária.
    """
    mensagens = [{"role": "system", "content": SYSTEM_PROMPT}] + historico

    for _ in range(MAX_TOOL_ITERATIONS):
        resposta = _client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=mensagens,
            tools=TOOLS_SCHEMA,
        )

        escolha = resposta.choices[0]
        mensagem = escolha.message

        if escolha.finish_reason == "tool_calls" and mensagem.tool_calls:
            mensagens.append(mensagem.model_dump(exclude_unset=True))

            for chamada in mensagem.tool_calls:
                nome = chamada.function.name
                try:
                    argumentos = json.loads(chamada.function.arguments or "{}")
                except json.JSONDecodeError:
                    argumentos = {}

                logger.info(f"Chamando ferramenta: {nome}({argumentos})")
                resultado = executar_ferramenta(nome, argumentos)

                mensagens.append({
                    "role": "tool",
                    "tool_call_id": chamada.id,
                    "content": resultado,
                })
            continue  # manda de novo pra IA já com o resultado da ferramenta

        return mensagem.content or "..."

    return "Desculpa, me enrolei tentando usar minhas ferramentas. Pode repetir a pergunta?"
