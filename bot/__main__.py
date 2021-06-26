import logging

from bot import root_path
from . import config
from .bot import Bot

logging.basicConfig(
    filename=None if config.debug else root_path / "logs.log",
    level=logging.WARNING if config.debug else logging.ERROR,
    format="%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s",
)


def load_extensions():
    cogs_path = root_path / "bot/cogs"
    ext_paths = (
        p for p in cogs_path.glob("*.py") if p.is_file() and not p.name.startswith("_")
    )
    return [f"bot.cogs.{p.stem}" for p in ext_paths]


bot = Bot()

for ext in load_extensions():
    bot.load_extension(ext)

bot.run()
