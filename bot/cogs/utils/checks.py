import datetime as dt

import pytz

from discord.ext import commands

from bot.context import BotContext
from .database_models import CooldownBucket


class OnDbCooldown(commands.CommandOnCooldown):
    retry_after: dt.datetime


def db_cooldown(rate: int, per: int):
    async def predicate(ctx: BotContext) -> bool:
        ctx.command.db_cooldown = True

        if ctx.invoked_with == "help":
            return True

        bucket = await CooldownBucket.get_or_none(
            guild_id=ctx.guild.id,
            member_id=ctx.author.id,
            command_name=ctx.command.qualified_name,
        )

        if bucket is None:
            bucket = await CooldownBucket.create(
                guild_id=ctx.guild.id,
                member_id=ctx.author.id,
                command_name=ctx.command.qualified_name,
            )

        now = dt.datetime.now()

        if bucket.window is not None and bucket.window.replace(
            tzinfo=pytz.UTC
        ) > now.replace(tzinfo=pytz.UTC):
            raise OnDbCooldown(bucket, bucket.window)

        bucket.uses += 1

        if bucket.uses >= rate:
            bucket.uses = 0
            bucket.window = now + dt.timedelta(seconds=per)

        await bucket.save()
        return True

    return commands.check(predicate)
