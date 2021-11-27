from typing import Union

import nextcord
from pydantic import BaseModel, Field, validator

from . import root_path


class StatusConfig(BaseModel):
    activity_type: Union[str, None] = Field("playing")
    status: str = Field("Default")

    @validator("activity_type")
    def validate_activity_type(cls, v):
        try:
            activity_type = getattr(nextcord.ActivityType, v.lower(), None)
            assert activity_type is not None, "Invalid activity type"
        except (TypeError, AttributeError):
            return None

        return activity_type.name


class BotConfig(BaseModel):
    __config_filenames__ = ("config_dev.json", "config.json")

    bot_token: str = Field("Токен бота из https://discord.com/developers")
    command_prefix: str = Field("!")

    status: StatusConfig = Field(StatusConfig())

    @classmethod
    def load_any(cls):
        for filename in cls.__config_filenames__:
            path = root_path / filename

            if path.exists():
                return cls.parse_file(path)
