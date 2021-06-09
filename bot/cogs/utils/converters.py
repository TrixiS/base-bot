import discord

from discord.ext import commands

from bot.context import BotContext


class NotAuthor(commands.MemberConverter):
    async def convert(self, ctx: BotContext, argument: str) -> discord.Member:
        member = await super().convert(ctx, argument)

        if member == ctx.author:
            raise commands.BadArgument(ctx.phrases.not_author)

        return member
