from bot import root_path

# Токен бота из https://discord.com/developers
bot_token: str = ""

# Префиксы команд бота
command_prefixes: list = ["!", "!!"]


# Системные переменные
debug: bool = False
database_url: str = f"sqlite://{root_path / 'database.sqlite3'}"
