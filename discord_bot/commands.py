from discord.ext import commands

from core import memory


def registrar_comandos(bot: commands.Bot):

    @bot.command(name="reset")
    async def reset(ctx: commands.Context):
        """Limpa o histórico de conversa deste usuário neste canal."""
        chave = memory.build_chave(ctx.channel.id, ctx.author.id)
        memory.limpar_historico(chave)
        await ctx.send(f"Histórico de conversa de {ctx.author.mention} neste canal foi limpo. ✅")
