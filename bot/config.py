from pydantic import BaseModel, Field

from . import root_path


class BaseBotConfig(BaseModel):
    __config_filenames__ = ("_config_dev.json", "config.json")

    bot_token: str = Field("Токен бота из https://discord.com/developers")
    command_prefix: str = Field("!")

    @classmethod
    def load_any(cls):
        for filepath in cls.__config_filepaths__():
            if filepath.exists():
                return cls.parse_file(filepath)

    @classmethod
    def __config_filepaths__(cls):
        for filename in cls.__config_filenames__:
            yield root_path / filename


class BotConfig(BaseBotConfig):
    ...
