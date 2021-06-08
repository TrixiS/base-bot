from .bot import Bot

bot = Bot()
cogs = ["bot.cogs.test"]

# TODO: setup logging
# "%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s"

for cog in cogs:
    bot.load_extension(cog)

bot.run()
