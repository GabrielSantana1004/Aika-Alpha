from discord.ext import commands

from core import memory


def registrar_comandos(bot: commands.Bot):

    @bot.command(name="reset")
    @commands.has_permissions(manage_messages=True)
    async def reset(ctx: commands.Context):
        """Limpa o histórico de conversa deste canal (afeta todo mundo)."""
        chave = memory.build_chave(ctx.channel.id)
        memory.limpar_historico(chave)
        await ctx.send("Histórico de conversa deste canal foi limpo. ✅")

    @reset.error
    async def reset_error(ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Só quem pode gerenciar mensagens nesse canal pode usar esse comando.")
        else:
            raise error
