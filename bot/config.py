from pydantic import BaseModel, Field

from . import root_path


class BaseBotConfig(BaseModel):
    __dev_config_filenames__ = ("config_dev.json",)
    __config_filenames__ = ("config.json",)

    bot_token: str = Field("Токен бота из https://discord.com/developers")
    command_prefix: str = Field("!")

    @classmethod
    def load_any(cls):
        all_config_filenames = (
            *cls.__dev_config_filenames__,
            *cls.__config_filenames__,
        )

        for filename in all_config_filenames:
            path = root_path / filename

            if path.exists():
                return cls.parse_file(path)


class OrmConfig(BaseModel):
    database_url: str = Field("sqlite://{sqlite_path}")


class BotConfig(BaseBotConfig):
    database: OrmConfig = Field(OrmConfig())
