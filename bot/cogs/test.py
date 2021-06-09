from discord.ext import commands

from .base_cog import BaseCog
from ..context import BotContext


class TestCog(BaseCog):
    @commands.command()
    async def test(self, ctx: BotContext):
        await ctx.answer("Hello World")


def setup(bot):
    bot.add_cog(TestCog(bot))
