from datetime import datetime, timedelta

import discord
from discord.ext import commands

from config import CANAIS_MONITORADOS, CANAL_LOG_ID, LOG_TTL_MINUTOS
from utils.logger import get_logger

logger = get_logger(__name__)

# Cache temporário: message_id -> dados da mensagem.
# Só guarda mensagens dos canais monitorados, e só por um tempo limitado.
_cache_mensagens: dict[int, dict] = {}


def _limpar_cache_expirado():
    limite = datetime.utcnow() - timedelta(minutes=LOG_TTL_MINUTOS)
    expirados = [mid for mid, dados in _cache_mensagens.items() if dados["hora"] < limite]
    for mid in expirados:
        _cache_mensagens.pop(mid, None)


def registrar_log_de_mensagens(bot: commands.Bot):
    if CANAL_LOG_ID is None or not CANAIS_MONITORADOS:
        logger.info("Log de mensagens apagadas desativado (CANAIS_MONITORADOS ou CANAL_LOG_ID não configurados).")
        return

    # @bot.listen permite coexistir com o on_message que já existe em events.py
    @bot.listen("on_message")
    async def guardar_mensagem(message: discord.Message):
        if message.author.bot:
            return
        if message.channel.id not in CANAIS_MONITORADOS:
            return

        _cache_mensagens[message.id] = {
            "autor_nome": str(message.author),
            "autor_avatar": message.author.display_avatar.url,
            "conteudo": message.content,
            "canal_id": message.channel.id,
            "anexos": [a.url for a in message.attachments],
            "hora": datetime.utcnow(),
        }
        _limpar_cache_expirado()

    @bot.event
    async def on_message_delete(message: discord.Message):
        if message.channel.id not in CANAIS_MONITORADOS:
            return

        canal_log = bot.get_channel(CANAL_LOG_ID)
        if canal_log is None:
            logger.error("CANAL_LOG_ID configurado não foi encontrado pelo bot.")
            return

        dados = _cache_mensagens.pop(message.id, None)

        if dados is None:
            await canal_log.send(
                f"🗑️ Uma mensagem foi apagada em <#{message.channel.id}>, mas eu não "
                f"tinha o conteúdo guardado (provavelmente antiga demais ou de antes "
                f"de eu reiniciar)."
            )
            return

        embed = discord.Embed(
            description=dados["conteudo"] or "*(mensagem sem texto — só anexo, provavelmente)*",
            color=0xFF2EC2,
            timestamp=dados["hora"],
        )
        embed.set_author(name=dados["autor_nome"], icon_url=dados["autor_avatar"])
        embed.set_footer(text=f"Mensagem apagada em #{message.channel}")

        if dados["anexos"]:
            embed.add_field(name="Anexos", value="\n".join(dados["anexos"]), inline=False)

        await canal_log.send(embed=embed)

    @bot.event
    async def on_bulk_message_delete(messages: list[discord.Message]):
        if not messages or messages[0].channel.id not in CANAIS_MONITORADOS:
            return

        canal_log = bot.get_channel(CANAL_LOG_ID)
        if canal_log is None:
            return

        for m in messages:
            _cache_mensagens.pop(m.id, None)

        await canal_log.send(
            f"🗑️ {len(messages)} mensagens foram apagadas de uma vez em "
            f"<#{messages[0].channel.id}>."
        )

    logger.info(f"Log de mensagens apagadas ativo para os canais: {CANAIS_MONITORADOS}")
