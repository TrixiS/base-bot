import discord

from discord.ext import commands

from bot.context import BotContext
from .utils.base_cog import BaseCog


class Tools(BaseCog):
    @commands.command()
    async def emoji(self, ctx: BotContext, emoji: discord.Emoji):
        await ctx.answer(f"```{str(emoji)}```")


def setup(bot):
    bot.add_cog(Tools(bot))
