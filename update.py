import argparse
from pathlib import Path

from pydantic import BaseModel

from bot import root_path
from bot.config import BotConfig
from bot.phrases import BotPhrases


def update_json_file_from_model(
    path: Path, model_cls: BaseModel, *, refresh: bool = False
):
    if refresh:
        model_object = model_cls()
    else:
        model_object = model_cls.parse_file(path)

    model_json = model_object.json(indent=2, ensure_ascii=False)

    with open(path, "w", encoding="utf-8") as f:
        f.write(model_json)


def create_json_file(filepath: Path):
    filepath.touch()
    filepath.write_text(r"{}")


def update_config_files(*, refresh: bool = False, create: bool = False):
    if refresh:
        filenames = BotConfig.__config_filenames__
    else:
        filenames = (
            *BotConfig.__dev_config_filenames__,
            *BotConfig.__config_filenames__,
        )

    for config_filename in filenames:
        config_path = root_path / config_filename

        if create and not config_path.exists():
            create_json_file(config_path)

        update_json_file_from_model(config_path, BotConfig, refresh=refresh)


def update_phrase_files(*, refresh: bool = False, create: bool = False):
    for phrases_path in (root_path / "phrases").glob("*.json"):
        if create and not phrases_path.exists():
            create_json_file(phrases_path)

        update_json_file_from_model(phrases_path, BotPhrases, refresh=refresh)


def main():
    class ArgsNamespace(argparse.Namespace):
        refresh: bool
        create: bool

    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        "--refresh", action="store_true", default=False, required=False
    )
    argument_parser.add_argument(
        "--create", action="store_true", default=False, required=False
    )

    args: ArgsNamespace = argument_parser.parse_args()

    update_config_files(refresh=args.refresh, create=args.create)
    update_phrase_files(refresh=args.refresh, create=args.create)


if __name__ == "__main__":
    main()
