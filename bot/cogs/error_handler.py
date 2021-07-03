import traceback

from typing import List

from discord.ext import commands

from .utils.base_cog import BaseCog
from ..context import BotContext


class ErrorHandler(BaseCog):
    def format_permissions(self, permissions: List[str]) -> str:
        return ", ".join(f"**{p.upper()}**" for p in permissions)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: BotContext, error: commands.CommandError):
        if isinstance(error, commands.BotMissingPermissions):
            return await ctx.answer(
                ctx.phrases.bot_missions_permissions.format(
                    bot=ctx.bot,
                    permissions=self.format_permissions(error.missing_perms),
                )
            )

        if isinstance(error, commands.MissingPermissions):
            return await ctx.answer(
                ctx.phrases.missing_permissions.format(
                    permissions=self.format_permissions(error.missing_perms)
                )
            )

        if isinstance(
            error,
            (
                commands.MissingRequiredArgument,
                commands.BadArgument,
                commands.CheckFailure,
            ),
        ):
            return await ctx.answer(str(error))

        formated_exc = traceback.format_exception(
            type(error), error, error.__traceback__
        )
        self.bot.logger.error("".join(formated_exc))


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
