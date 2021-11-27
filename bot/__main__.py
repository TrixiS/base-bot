import argparse
import logging
import os
import re
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


def cog_path_from_name(cogs_path: Path, cog_name: str) -> Path:
    name_words = re.findall("[A-Z][^A-Z]*", cog_name)
    cog_filename = "_".join(map(str.lower, name_words)) + ".py"
    return cogs_path / cog_filename


def create_cog(cogs_path: Path, cog_name: str) -> Path:
    cog_path = cog_path_from_name(cogs_path, cog_name)

    if cog_path.exists():
        return cog_path

    cog_code = f"""import nextcord

from nextcord.ext import commands

from bot.context import BotContext
from .utils.base_cog import BaseCog


class {cog_name}(BaseCog):
    pass


def setup(bot):
    bot.add_cog({cog_name}(bot))"""

    cog_path.write_text(cog_code, encoding="utf-8")
    return cog_path


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--cog", help="Name of a cog to create")
    arg_parser.add_argument(
        "--jump", action="store_true", help="Jump to cog file (VSCode only)"
    )
    args = arg_parser.parse_args()

    cogs_path = root_path / "bot/cogs"

    if args.cog:
        cog_path = create_cog(cogs_path, args.cog)

        if args.jump:
            os.system(f"code {cog_path.absolute()}")

        return

    config = BotConfig.load_any()
    phrases = BotPhrases.load_all()

    logging.basicConfig(
        filename="logs.log",
        level=logging.ERROR,
        format="%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s",
    )

    bot = Bot(config, phrases)

    for ext in get_all_extensions(cogs_path):
        bot.load_extension(ext)

    bot.run()


main()
