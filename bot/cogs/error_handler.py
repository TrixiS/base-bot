import traceback

from discord.ext import commands

from ..bot import Bot
from ..context import BotContext
from .utils.base_cog import BaseCog


class ErrorHandler(BaseCog):
    @commands.Cog.listener()
    async def on_command_error(self, ctx: BotContext, error: commands.CommandError):
        if isinstance(
            error,
            (
                commands.MissingRequiredArgument,
                commands.BadArgument,
            ),
        ):
            return await ctx.answer(str(error))

        formated_exc = traceback.format_exception(
            type(error), error, error.__traceback__
        )

        self.bot.logger.error("".join(formated_exc))


async def setup(bot: Bot):
    await bot.add_cog(ErrorHandler(bot))
