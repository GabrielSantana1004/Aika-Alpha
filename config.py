import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
MAX_HISTORY_MESSAGES = int(os.getenv("MAX_HISTORY_MESSAGES", "20"))


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
