import json

from typing import List

from pydantic import BaseModel, Field

from bot import root_path


class ErrorPhrases(BaseModel):
    cant_use: str = Field("Вы не можете использовать эту команду")


class OwnerPhrases(BaseModel):
    ext_loaded: str = Field("{ext} успешно загружено")
    ext_unloaded: str = Field("{ext} успешно выгружено")
    ext_reloaded: str = Field("{ext} успешно перезагружено")
    bot_close: str = Field("{bot.user.name} выключается")


class DefaultPhrases(BaseModel):
    bot_started: str = Field("Бот {bot.user} успешно запущен")


class BotPhrases(BaseModel):
    __lang_code__: str = None
    default: DefaultPhrases = Field(DefaultPhrases())
    errors: ErrorPhrases = Field(ErrorPhrases())
    owner: OwnerPhrases = Field(OwnerPhrases())

    @classmethod
    def load_all(cls) -> List["BotPhrases"]:
        phrases_dir = root_path / "phrases"
        parsed_phrases: List[BotPhrases] = []

        for phrases_path in phrases_dir.glob("*.json"):
            try:
                phrases = BotPhrases.parse_file(phrases_path)
            except json.decoder.JSONDecodeError:
                continue

            parsed_phrases.append(phrases)

        return parsed_phrases
