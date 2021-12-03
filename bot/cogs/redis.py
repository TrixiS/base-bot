import aioredis

from .utils.base_cog import BaseCog


class Redis(BaseCog):
    def __init__(self, *args):
        super().__init__(*args)
        self.redis = aioredis.Redis(
            **self.bot.config.redis.dict(), decode_responses=True
        )


def setup(bot):
    bot.add_cog(Redis(bot))
