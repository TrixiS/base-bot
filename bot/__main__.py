import asyncio
import logging
from pathlib import Path

from bot import root_path

from .bot import Bot
from .config import BotConfig
from .phrases import BotPhrases


def get_all_extensions(cogs_path: Path):
    ext_paths = (
        p for p in cogs_path.glob("*.py") if p.is_file() and not p.name.startswith("_")
    )

    return [f"bot.cogs.{p.stem}" for p in ext_paths]


async def main():
    config = BotConfig.load_any()
    phrases = BotPhrases.load_all()

    logging.basicConfig(filename="logs.log", level=logging.ERROR)

    bot = Bot(config, phrases)

    for ext in get_all_extensions(root_path / "bot/cogs"):
        await bot.load_extension(ext)

    await bot.start(bot.config.bot_token)


asyncio.run(main())
