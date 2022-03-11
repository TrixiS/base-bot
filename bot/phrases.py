from typing import List

from pydantic import BaseModel, Field

from bot import root_path


class DefaultPhrases(BaseModel):
    bot_started: str = Field("Бот {bot.user} успешно запущен")


class BaseBotPhrases(BaseModel):
    default: DefaultPhrases = Field(DefaultPhrases())

    @classmethod
    def load_all(cls) -> List["BotPhrases"]:
        parsed_phrases: List[BotPhrases] = []

        for phrases_path in cls.__phrases_filepaths__():
            phrases = BotPhrases.parse_file(phrases_path)
            parsed_phrases.append(phrases)

        return parsed_phrases

    @classmethod
    def __phrases_filepaths__(cls):
        yield from (root_path / "phrases").glob("*.json")


class BotPhrases(BaseBotPhrases):
    ...
