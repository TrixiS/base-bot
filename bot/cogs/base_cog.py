from discord.ext import commands

from bot.bot import Bot


class BaseCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def on_bot_close(self):
        pass
