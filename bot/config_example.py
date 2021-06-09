from pathlib import Path

# Токен бота из https://discord.com/developers
bot_token: str = ""

# Прекфиксы команд бота
command_prefixes: list = ["!", "!!"]


# Системные переменные
debug: bool = False
database_url: str = f"sqlite://{Path(__file__).parent / '../database.sqlite3'}"
