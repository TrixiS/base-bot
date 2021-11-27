import ast

import nextcord
from nextcord.ext import commands

from bot.context import BotContext
from .utils.base_cog import BaseCog


def is_owner():
    async def predicate(ctx: BotContext):
        if await ctx.bot.is_owner(ctx.author):
            return True

        app = await ctx.bot.application_info()

        if app.team is not None:
            team_member = nextcord.utils.find(
                lambda m: m.id == ctx.author.id, app.team.members
            )

            if team_member is not None:
                return True

        raise commands.CheckFailure(ctx.phrases.errors.cant_use)

    return commands.check(predicate)


def insert_returns(body):
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)


class Owner(BaseCog):
    @is_owner()
    @commands.command()
    async def load(self, ctx: BotContext, ext: str):
        self.bot.load_extension(ext)
        await ctx.answer(ctx.phrases.owner.ext_loaded.format(ext=ext))

    @is_owner()
    @commands.command()
    async def unload(self, ctx: BotContext, ext: str):
        self.bot.unload_extension(ext)
        await ctx.answer(ctx.phrases.owner.ext_unloaded.format(ext=ext))

    @is_owner()
    @commands.command()
    async def reload(self, ctx: BotContext, ext: str):
        self.bot.reload_extension(ext)
        await ctx.answer(ctx.phrases.owner.ext_reloaded.format(ext=ext))

    @is_owner()
    @commands.command()
    async def eval(self, ctx: BotContext, *, code: str):
        fmt = "```Python\n{}```"
        fn_name = "_eval_expr"

        cmd = code.strip("` ")
        cmd = "\n".join(f"	{i}" for i in cmd.splitlines())

        body = f"async def {fn_name}():\n{cmd}"
        parsed = ast.parse(body)
        body = parsed.body[0].body

        insert_returns(body)

        env = {
            "bot": ctx.bot,
            "nextcord": nextcord,
            "command": nextcord.ext.commands,
            "ctx": ctx,
            "__import__": __import__,
            "__name__": __name__,
        }

        exec(compile(parsed, filename="<ast>", mode="exec"), env)

        try:
            result = await eval(f"{fn_name}()", env)
            await ctx.answer(fmt.format(result))
        except Exception as e:
            await ctx.answer(fmt.format(f"{type(e).__name__}: {e}"))

    @is_owner()
    @commands.command()
    async def kill(self, ctx: BotContext):
        await ctx.answer(ctx.phrases.owner.bot_close.format(bot=ctx.bot))
        await ctx.bot.close()


def setup(bot):
    bot.add_cog(Owner(bot))
