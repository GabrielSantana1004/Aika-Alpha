import discord
from discord.ext import commands

from core import memory
from core.ai_client import gerar_resposta
from utils.logger import get_logger

logger = get_logger(__name__)


async def eh_resposta_ao_bot(message: discord.Message, bot: commands.Bot) -> bool:
    """Verifica se a mensagem é uma reply a uma mensagem do próprio bot,
    independente do toggle de @menção do Discord estar ligado ou não."""
    if message.reference is None:
        return False

    resolved = message.reference.resolved
    if resolved is None:
        try:
            resolved = await message.channel.fetch_message(message.reference.message_id)
        except (discord.NotFound, discord.Forbidden, discord.HTTPException):
            return False

    return isinstance(resolved, discord.Message) and resolved.author.id == bot.user.id


def registrar_eventos(bot: commands.Bot):

    @bot.event
    async def on_ready():
        logger.info(f"Conectado como {bot.user} (id: {bot.user.id})")

    @bot.event
    async def on_message(message: discord.Message):
        if message.author.bot:
            return

        # deixa comandos tipo "!reset" seguirem o fluxo normal do discord.py
        if message.content.startswith(bot.command_prefix):
            await bot.process_commands(message)
            return

        mencionado = bot.user in message.mentions
        respondendo_o_bot = await eh_resposta_ao_bot(message, bot)

        if not mencionado and not respondendo_o_bot:
            return

        conteudo = message.content
        for formato in (f"<@{bot.user.id}>", f"<@!{bot.user.id}>"):
            conteudo = conteudo.replace(formato, "").strip()

        if not conteudo:
            await message.reply("Fala! Me chamou, pode falar o que precisa.")
            return

        chave_historico = memory.build_chave(message.channel.id, message.author.id)
        memory.adicionar_mensagem(chave_historico, "user", conteudo)

        async with message.channel.typing():
            historico = memory.get_historico(chave_historico)
            try:
                resposta = gerar_resposta(historico)
            except Exception as e:
                logger.error(f"Erro ao gerar resposta: {e}")
                resposta = "Deu ruim aqui do meu lado agora, tenta de novo daqui a pouco."

        memory.adicionar_mensagem(chave_historico, "assistant", resposta)

        await message.reply(resposta[:2000])  # limite de caracteres do Discord
