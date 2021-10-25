import json

from pathlib import Path

from bot import root_path
from bot.config import BotConfig
from bot.phrases import BotPhrases
from pydantic import BaseModel


def update_phrases_file_from_model(path: Path, model_cls: BaseModel):
    if not path.exists():
        return

    try:
        model_object = model_cls.parse_file(path)
    except json.decoder.JSONDecodeError:
        model_object = model_cls()

    with open(path, "w", encoding="utf-8") as f:
        json_string = model_object.json(indent=2, ensure_ascii=False)
        f.write(json_string)


def main():
    for config_filename in BotConfig.__config_filenames__:
        update_phrases_file_from_model(root_path / config_filename, BotConfig)

    for phrases_path in (root_path / "phrases").glob("*.json"):
        update_phrases_file_from_model(phrases_path, BotPhrases)


if __name__ == "__main__":
    main()
