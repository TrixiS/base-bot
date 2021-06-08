from discord.ext import commands

from .base_cog import BaseCog


class TestCog(BaseCog):

    @commands.Cog.listener()
    async def on_ready(self):
        print("Hello World")


def setup(bot):
    bot.add_cog(TestCog(bot))
