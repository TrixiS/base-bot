from typing import List

from pydantic import BaseModel, Field

from bot import root_path


class ErrorPhrases(BaseModel):
    on_cooldown: str = Field("Команда на кулдауне. Попробуйте снова **{date}**")


class CooldownPhrases(BaseModel):
    cooldown_seconds_fmt: str = Field("через {seconds}с")
    cooldown_minutes_fmt: str = Field("через {minutes}м {seconds}с")
    cooldown_hours_fmt: str = Field("через {hours}ч {minutes}м")
    cooldown_days_fmt: str = Field("через {days}д {hours}ч")


class DefaultPhrases(BaseModel):
    bot_started: str = Field("Бот {bot.user} успешно запущен")


class BotPhrases(BaseModel):
    __lang_code__: str = None
    default: DefaultPhrases = Field(DefaultPhrases())
    errors: ErrorPhrases = Field(ErrorPhrases())
    cooldown: CooldownPhrases = Field(CooldownPhrases())

    @classmethod
    def load_all(cls) -> List["BotPhrases"]:
        phrases_dir = root_path / "phrases"
        parsed_phrases: List[BotPhrases] = []

        for phrases_path in phrases_dir.glob("*.json"):
            phrases = BotPhrases.parse_file(phrases_path)
            parsed_phrases.append(phrases)

        return parsed_phrases
