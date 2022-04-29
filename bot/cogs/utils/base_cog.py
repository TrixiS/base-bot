from bot.bot import Bot
from nextcord.ext import commands


class BaseCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.bot.loop.create_task(self.on_startup())

    def _inject_cogs(self):
        for name, cls in self.__annotations__.items():
            if not issubclass(cls, BaseCog):
                continue

            cog = self.bot.get_cog(cls.__name__)
            setattr(self, name, cog)

    async def on_shutdown(self):
        pass

    async def on_startup(self):
        self._inject_cogs()
