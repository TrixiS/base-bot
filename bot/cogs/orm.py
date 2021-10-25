from tortoise import Tortoise

from bot import root_path
from .utils.base_cog import BaseCog


class Orm(BaseCog):
    def __init__(self, *args):
        super().__init__(*args)

    async def on_bot_close(self):
        await Tortoise.close_connections()

    async def on_startup(self):
        sqlite_path = root_path / "database.sqlite3"

        await Tortoise.init(
            db_url=self.bot.config.database.database_url.format(
                sqlite_path=sqlite_path
            ),
            modules={"models": ["bot.cogs.utils.database_models"]},
        )

        await Tortoise.generate_schemas(safe=True)


def setup(bot):
    bot.add_cog(Orm(bot))
