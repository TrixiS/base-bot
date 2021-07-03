import discord

from discord.ext import commands

from bot.context import BotContext
from .utils.base_cog import BaseCog
from .utils.converters import RangedIntConverter as Range


class Moderation(BaseCog):
    def __init__(self, *args):
        super().__init__(*args)
        self.clearing_channels = []

    @commands.bot_has_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    @commands.command(aliases=["clean", "purge"])
    async def clear(
        self,
        ctx: BotContext,
        amount: Range(1, 1000),
        *,
        channel: discord.TextChannel = None
    ):
        channel = channel or ctx.channel

        if channel.id in self.clearing_channels:
            return

        self.clearing_channels.append(channel.id)

        deleted_messages = await channel.purge(limit=amount + 1)
        await channel.send(
            ctx.phrases.deleted_messages.format(
                deleted=len(deleted_messages) - 1, amount=amount
            ),
            delete_after=10,
        )

        self.clearing_channels.remove(channel.id)


def setup(bot):
    bot.add_cog(Moderation(bot))
