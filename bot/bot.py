import logging
from typing import List

import discord
from discord.ext import commands

from .config import BotConfig
from .context import BotContext
from .phrases import BotPhrases

# TODO: put logger into error_handler cog


class Bot(commands.AutoShardedBot):
    def __init__(self, config: BotConfig, phrases: List[BotPhrases]):
        super().__init__(
            command_prefix=get_command_prefix, intents=discord.Intents.all()
        )
        self.logger = logging.getLogger("bot")
        self.config = config
        self.phrases = phrases

    @property
    def default_phrases(self) -> BotPhrases:
        return self.phrases[0]

    async def start(self, token: str, *, reconnect: bool = True) -> None:
        for cog in self.cogs.values():
            await cog.on_startup()

        await super().start(token=token, reconnect=reconnect)

    async def close(self):
        for cog in self.cogs.values():
            await cog.on_shutdown()

        await super().close()

    async def get_context(self, message: discord.Message) -> BotContext:
        return await super().get_context(message, cls=BotContext)

    async def process_commands(self, message: discord.Message):
        ctx = await self.get_context(message)

        if ctx.command is None:
            return

        await self.invoke(ctx)

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        await self.process_commands(message)

    async def on_ready(self):
        print(self.default_phrases.default.bot_started.format(bot=self))


async def get_command_prefix(bot: Bot, message: discord.Message) -> str:
    return bot.config.command_prefix
