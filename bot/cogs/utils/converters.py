import textwrap

from enum import Enum

import discord

from discord.ext import commands

from bot.context import BotContext


class SafeBadArgument(commands.BadArgument):
    def format_argument(self, argument: str) -> str:
        placeholder = f"{argument[:3]}..."
        return textwrap.shorten(
            argument, width=len(placeholder), placeholder=placeholder
        )

    def __init__(self, message: str, argument: str, *args, **fmt_kwargs):
        super().__init__(
            *args,
            message=message.format(
                argument=self.format_argument(argument),
                **fmt_kwargs,
            ),
        )


class NotAuthor(commands.MemberConverter):
    async def convert(self, ctx: BotContext, argument: str) -> discord.Member:
        member = await super().convert(ctx, argument)

        if member == ctx.author:
            raise commands.BadArgument(ctx.phrases.errors.not_author)

        return member


class IntConverter(commands.Converter):
    async def convert(self, ctx: BotContext, argument: str):
        try:
            return int(argument)
        except ValueError:
            raise SafeBadArgument(ctx.phrases.errors.invalid_int, argument)


class RangedIntConverter(IntConverter):
    def __init__(
        self,
        start: int = None,
        stop: int = None,
        step: int = 1,
        *,
        argument_range: range = None,
    ):
        if argument_range is not None:
            self.argument_range = argument_range
            return

        self.argument_range = range(start, stop + 1, step)

    async def convert(self, ctx: BotContext, argument: str):
        number = await super().convert(ctx, argument)

        if number in self.argument_range:
            return number

        raise SafeBadArgument(
            ctx.phrases.errors.int_not_in_range,
            argument,
            range=range(self.argument_range.start, self.argument_range.stop - 1),
        )


class EnumConverter(commands.Converter):
    def __init__(self, enum: Enum, convert_from_values: bool = False):
        self.enum = enum
        self.convert_from_values = convert_from_values

    async def convert(self, ctx: BotContext, argument: str):
        for name, value in self.enum.__members__.items():
            if (
                self.convert_from_values and argument == str(value.value)
            ) or argument == name:
                return value

        values = (
            [v.value for v in self.enum.__members__.values()]
            if self.convert_from_values
            else self.enum.__members__.keys()
        )

        raise SafeBadArgument(
            ctx.phrases.errors.invalid_enum_value,
            argument,
            values=" | ".join(f"`{v}`" for v in values),
        )
