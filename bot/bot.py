import logging

from typing import List

import discord

from discord.ext import commands

from .phrases import BotPhrases
from .config import BotConfig
from .context import BotContext


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
        default_language: str = getattr(self.config, "default_language", "ru")
        phrases = discord.utils.find(
            lambda p: p.__lang_code__ == default_language, self.phrases
        )

        if phrases is None:
            return self.phrases[0]

        return phrases

    def run(self):
        super().run(self.config.bot_token, bot=True)

    async def close(self):
        for cog in self.cogs.values():
            await cog.on_bot_close()

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


async def get_command_prefix(bot: Bot, message: discord.Message) -> List[str]:
    return bot.config.command_prefix
