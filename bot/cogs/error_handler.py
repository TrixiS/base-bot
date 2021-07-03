import traceback
import datetime as dt

import pytz

from discord.ext import commands

from .utils.base_cog import BaseCog
from .utils.checks import OnDbCooldown
from .utils.database_models import CooldownBucket
from ..context import BotContext


class ErrorHandler(BaseCog):
    async def remove_cooldown_use(self, ctx: BotContext, command: commands.Command):
        bucket = await CooldownBucket.get_or_none(
            guild_id=ctx.guild.id,
            member_id=ctx.author.id,
            command_name=command.qualified_name,
        )

        if bucket is None or bucket.uses == 0:
            return

        bucket.uses = bucket.uses - 1
        await bucket.save()

    def format_cooldown(self, ctx: BotContext, window: dt.datetime) -> str:
        now = dt.datetime.now()
        delta = window.replace(tzinfo=pytz.UTC) - now.replace(tzinfo=pytz.UTC)
        total_seconds = delta.total_seconds()

        if total_seconds < 60:
            fmt = ctx.phrases.cooldown_seconds_fmt
        elif window.day > now.day:
            fmt = ctx.phrases.cooldown_date_fmt
        else:
            fmt = ctx.phrases.cooldown_minutes_fmt

        return window.strftime(fmt)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: BotContext, error: commands.CommandError):
        if isinstance(
            error,
            (
                commands.MissingRequiredArgument,
                commands.BadArgument,
                commands.CheckFailure,
            ),
        ):
            if hasattr(ctx.command, "db_cooldown") and ctx.command.db_cooldown:
                await self.remove_cooldown_use(ctx, ctx.command)

            return await ctx.answer(str(error))

        if isinstance(error, commands.CommandOnCooldown):
            retry_datetime = (
                error.retry_after
                if isinstance(error, OnDbCooldown)
                else dt.datetime.now() + dt.timedelta(seconds=error.retry_after)
            )

            return await ctx.answer(
                ctx.phrases.on_cooldown.format(
                    date=self.format_cooldown(ctx, retry_datetime)
                )
            )

        formated_exc = traceback.format_exception(
            type(error), error, error.__traceback__
        )
        self.bot.logger.error("".join(formated_exc))


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
