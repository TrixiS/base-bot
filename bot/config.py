from pydantic import BaseModel, Field

from . import root_path


class RedisConfig(BaseModel):
    host: str = Field("")
    port: int = Field(6379)
    password: str = Field("")
    db: int = Field(0)


class BotConfig(BaseModel):
    __config_filenames__ = ("config_dev.json", "config.json")

    bot_token: str = Field("Токен бота из https://discord.com/developers")
    command_prefix: str = Field("!")
    redis: RedisConfig = Field(RedisConfig())

    @classmethod
    def load_any(cls):
        for filename in cls.__config_filenames__:
            path = root_path / filename

            if path.exists():
                return cls.parse_file(path)
