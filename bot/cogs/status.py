import discord

from discord.ext import commands

from .utils.base_cog import BaseCog


class Status(BaseCog):
    def __init__(self, *args):
        super().__init__(*args)
        self.bot.loop.create_task(self.set_activity())

    def cog_unload(self):
        async def remove_activity():
            await self.bot.change_presence(activity=None)

        self.bot.loop.create_task(remove_activity())

    async def set_activity(self):
        await self.bot.wait_until_ready()

        if self.bot.config.activity_type is None or not self.bot.config.status:
            return

        activity = discord.Activity(
            name=self.bot.config.status, type=self.bot.config.activity_type
        )

        await self.bot.change_presence(activity=activity)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.set_activity()


def setup(bot):
    bot.add_cog(Status(bot))
