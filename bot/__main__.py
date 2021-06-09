import logging

from pathlib import Path

from . import config
from .bot import Bot

logging.basicConfig(
    filename=None if config.debug else Path(__file__).parent / "../logs.log",
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s",
)

bot = Bot()
cogs = []

for cog in cogs:
    bot.load_extension(cog)

bot.run()
