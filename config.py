import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-sol")
#OPENAI_MODEL= os.getenv("OPENAI_MODEL_LUNA", "gpt-5.6-luna")
MAX_HISTORY_MESSAGES = int(os.getenv("MAX_HISTORY_MESSAGES", "20"))

# Log de mensagens apagadas — IDs separados por vírgula no .env
CANAIS_MONITORADOS = [
    int(cid) for cid in os.getenv("CANAIS_MONITORADOS", "").split(",") if cid.strip()
]
_canal_log = os.getenv("CANAL_LOG_ID", "").strip()
CANAL_LOG_ID = int(_canal_log) if _canal_log else None
LOG_TTL_MINUTOS = int(os.getenv("LOG_TTL_MINUTOS", "180"))


def validate_config():
    """Avisa no console quais variáveis obrigatórias estão faltando no .env."""
    faltando = []
    if not DISCORD_TOKEN:
        faltando.append("DISCORD_TOKEN")
    if not OPENAI_API_KEY:
        faltando.append("OPENAI_API_KEY")
    if not TAVILY_API_KEY:
        faltando.append("TAVILY_API_KEY (a pesquisa na web não vai funcionar sem ela)")

    if faltando:
        print("[AVISO] Variáveis não configuradas no .env:")
        for item in faltando:
            print(f"  - {item}")
