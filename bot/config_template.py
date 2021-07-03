from discord import ActivityType


# Токен бота из https://discord.com/developers
bot_token: str = ""

# Префиксы команд бота
command_prefixes: list = ["!", "!!"]

# Тип статуса
activity_type = ActivityType.listening

# Текст статуса
status: str = ""


# Системные переменные
debug: bool = False
