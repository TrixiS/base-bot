import nextcord
from nextcord.ext import commands

from .utils.base_cog import BaseCog


class Status(BaseCog):
    def cog_unload(self):
        self.bot.loop.create_task(self.bot.change_presence(activity=None))

    async def on_startup(self):
        await self.set_activity()

    async def set_activity(self):
        await self.bot.wait_until_ready()

        if (
            self.bot.config.status.activity_type is None
            or not self.bot.config.status.status
            or (
                converted_activity := getattr(
                    nextcord.ActivityType, self.bot.config.status.activity_type, None
                )
            )
            is None
        ):
            return

        activity = nextcord.Activity(
            name=self.bot.config.status.status,
            type=converted_activity,
        )

        await self.bot.change_presence(activity=activity)


def setup(bot):
    bot.add_cog(Status(bot))
