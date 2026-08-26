from collections import defaultdict, deque

from config import MAX_HISTORY_MESSAGES

# Histórico compartilhado por CANAL — todo mundo que conversa com a Aika no
# mesmo canal cai na mesma linha do tempo. Quem falou o quê é diferenciado
# pelo nome incluído no próprio conteúdo da mensagem (veja adicionar_mensagem).
# Perdido se o bot reiniciar; se um dia quiser persistência entre reinícios,
# é só trocar esse dicionário por leitura/escrita em arquivo JSON ou banco.
_historicos = defaultdict(lambda: deque(maxlen=MAX_HISTORY_MESSAGES))


def build_chave(canal_id) -> int:
    """Chave do histórico: agora é só o canal, compartilhado entre usuários."""
    return canal_id


def get_historico(chave) -> list[dict]:
    return list(_historicos[chave])


def adicionar_mensagem_usuario(chave, autor_nome: str, content: str):
    """Adiciona uma fala de um usuário, prefixada com o nome dele — é assim
    que a IA diferencia quem está falando dentro de um histórico compartilhado."""
    _historicos[chave].append({"role": "user", "content": f"{autor_nome}: {content}"})


def adicionar_mensagem_assistente(chave, content: str):
    _historicos[chave].append({"role": "assistant", "content": content})


def limpar_historico(chave):
    _historicos[chave].clear()
