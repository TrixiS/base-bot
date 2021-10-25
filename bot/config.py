from pydantic import BaseModel, Field

from . import root_path


class OrmConfig(BaseModel):
    database_url: str = Field("sqlite://{sqlite_path}")


class BotConfig(BaseModel):
    __config_filenames__ = ("config_dev.json", "config.json")

    bot_token: str = Field("Токен бота из https://discord.com/developers")
    command_prefix: str = Field("!")
    database: OrmConfig = Field(OrmConfig())

    @classmethod
    def load_any(cls):
        for filename in cls.__config_filenames__:
            path = root_path / filename

            if path.exists():
                return cls.parse_file(path)
