from discord.ext import commands
from tortoise import Tortoise

from .base_cog import BaseCog


class OrmCog(BaseCog):
    def __init__(self, *args):
        super().__init__(*args)
        self.tortoise_inited = False

    async def init_tortoise(self):
        await Tortoise.init(
            db_url=self.bot.config.database_url,
            modules={"models": ["bot.cogs.utils.database_models"]},
        )

        await Tortoise.generate_schemas(safe=True)

    async def on_bot_close(self):
        await Tortoise.close_connections()

    @commands.Cog.listener()
    async def on_ready(self):
        if self.tortoise_inited:
            return

        await self.init_tortoise()
        self.tortoise_inited = True


def setup(bot):
    bot.add_cog(OrmCog(bot))
