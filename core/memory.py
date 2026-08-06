from collections import defaultdict, deque

from config import MAX_HISTORY_MESSAGES

# Histórico separado por (canal, usuário) — cada pessoa tem sua própria
# conversa com a IA, mesmo que várias mensagens aconteçam no mesmo canal.
# Perdido se o bot reiniciar; se um dia quiser persistência entre reinícios,
# é só trocar esse dicionário por leitura/escrita em arquivo JSON ou banco.
_historicos = defaultdict(lambda: deque(maxlen=MAX_HISTORY_MESSAGES))


def build_chave(canal_id, usuario_id) -> tuple:
    """Monta a chave usada pra identificar o histórico de um usuário em um canal."""
    return (canal_id, usuario_id)


def get_historico(chave) -> list[dict]:
    return list(_historicos[chave])


def adicionar_mensagem(chave, role: str, content: str):
    _historicos[chave].append({"role": role, "content": content})


def limpar_historico(chave):
    _historicos[chave].clear()
