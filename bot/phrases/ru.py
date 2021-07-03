# Фразы бота
bot_started: str = "Бот {bot.user} успешно запущен"

# Ошибки
not_author: str = "Вы не можете использовать эту команду на себя"
cant_use: str = "Вы не можете использовать эту команду"
invalid_int: str = "Вы ввели неверное число - **{argument}**"
int_not_in_range: str = (
    "Число **{argument}** не находится в диапазоне **{range.start}-{range.stop}**"
)
invalid_enum_value: str = (
    "Вместо **{argument}** необходимо указать одно из значений: {values}"
)
