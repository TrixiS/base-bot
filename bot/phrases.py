from typing import List

from pydantic import BaseModel, Field

from bot import root_path


class ErrorPhrases(BaseModel):
    not_author: str = Field("Вы не можете использовать эту команду на себя")
    cant_use: str = Field("Вы не можете использовать эту команду")
    invalid_int: str = Field("Вы ввели неверное число - **{argument}**")
    int_not_in_range: str = Field(
        "Число **{argument}** не находится в диапазоне **{range.start}-{range.stop}**"
    )
    invalid_enum_value: str = Field(
        "Вместо **{argument}** необходимо указать одно из значений: {values}"
    )


class DefaultPhrases(BaseModel):
    bot_started: str = Field("Бот {bot.user} успешно запущен")


class BotPhrases(BaseModel):
    __lang_code__: str = None
    default: DefaultPhrases = Field(DefaultPhrases())
    errors: ErrorPhrases = Field(ErrorPhrases())

    @classmethod
    def load_all(cls) -> List["BotPhrases"]:
        phrases_dir = root_path / "phrases"
        parsed_phrases: List[BotPhrases] = []

        for phrases_path in phrases_dir.glob("*.json"):
            phrases = BotPhrases.parse_file(phrases_path)
            parsed_phrases.append(phrases)

        return parsed_phrases
