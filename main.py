import discord
from discord.ext import commands

from config import DISCORD_TOKEN, validate_config
from discord_bot.events import registrar_eventos
from discord_bot.commands import registrar_comandos
from utils.logger import get_logger

logger = get_logger(__name__)


def main():
    validate_config()

    intents = discord.Intents.default()
    intents.message_content = True  # necessário pra ler o conteúdo das mensagens
    intents.members = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    registrar_eventos(bot)
    registrar_comandos(bot)

    if not DISCORD_TOKEN:
        logger.error("DISCORD_TOKEN não configurado. Confira seu arquivo .env.")
        return

    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
