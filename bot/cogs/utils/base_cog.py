import inspect

from bot.bot import Bot
from discord.ext import commands


class BaseCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    def _inject_cogs(self):
        for name, cls in self.__annotations__.items():
            if not inspect.isclass(cls) or not issubclass(cls, BaseCog):
                continue

            cog = self.bot.get_cog(cls.__name__)
            setattr(self, name, cog)

    async def on_shutdown(self):
        pass

    async def on_startup(self):
        self._inject_cogs()
