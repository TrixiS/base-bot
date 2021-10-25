import traceback
import datetime as dt

import pytz

from tortoise.expressions import F
from discord.ext import commands

from .utils.base_cog import BaseCog
from .utils.checks import OnDbCooldown
from .utils.database_models import CooldownBucket
from ..context import BotContext


class ErrorHandler(BaseCog):
    async def remove_cooldown_use(self, ctx: BotContext, command: commands.Command):
        await CooldownBucket.filter(
            guild_id=ctx.guild.id,
            member_id=ctx.author.id,
            command_name=command.qualified_name,
            uses__gt=0,
        ).update(uses=F("uses") - 1)

    def format_cooldown(self, ctx: BotContext, window: dt.datetime) -> str:
        now = dt.datetime.utcnow()
        delta = window.replace(tzinfo=pytz.UTC) - now.replace(tzinfo=pytz.UTC)
        total_seconds = delta.total_seconds()

        minutes, seconds = map(int, divmod(total_seconds, 60))
        hours, minutes = map(int, divmod(minutes, 60))
        days, hours = map(int, divmod(hours, 24))

        if days > 0:
            fmt = ctx.phrases.cooldown.cooldown_days_fmt
        elif hours > 0:
            fmt = ctx.phrases.cooldown.cooldown_hours_fmt
        elif minutes > 0:
            fmt = ctx.phrases.cooldown.cooldown_minutes_fmt
        else:
            fmt = ctx.phrases.cooldown.cooldown_seconds_fmt

        return fmt.format(seconds=seconds, minutes=minutes, hours=hours, days=days)

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
            if getattr(ctx.command, "__db_cooldown__", False):
                await self.remove_cooldown_use(ctx, ctx.command)

            return await ctx.answer(str(error))

        if isinstance(error, commands.CommandOnCooldown):
            retry_datetime = (
                error.retry_after
                if isinstance(error, OnDbCooldown)
                else dt.datetime.utcnow() + dt.timedelta(seconds=error.retry_after)
            )

            return await ctx.answer(
                ctx.phrases.errors.on_cooldown.format(
                    date=self.format_cooldown(ctx, retry_datetime)
                )
            )

        formated_exc = traceback.format_exception(
            type(error), error, error.__traceback__
        )
        self.bot.logger.error("".join(formated_exc))


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
