import os
import argparse
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


def run_bot():
    bot = Bot()

    for ext in load_extensions():
        bot.load_extension(ext)

    bot.run()


def create_cog(cog_name: str):
    cogs_path = root_path / "bot/cogs"
    cog_path = cogs_path / f"{cog_name.lower()}.py"

    if cog_path.exists():
        return

    cog_code = f"""import discord

from discord.ext import commands

from .utils.base_cog import BaseCog


class {cog_name}(BaseCog):
    pass


def setup(bot):
    bot.add_cog({cog_name}(bot))"""

    cog_path.write_text(cog_code, encoding="utf-8")
    return cog_path


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--cog")
    arg_parser.add_argument(
        "--move", action="store_true", default=False, required=False
    )
    args = arg_parser.parse_args()

    if args.cog:
        cog_path = create_cog(args.cog)

        if cog_path is None and not args.move:
            return print(f"Cog {args.cog} is already created.")

        if args.move:
            return os.system(f"code {cog_path.absolute()}")

    run_bot()


main()
