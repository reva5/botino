import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta

def cal_make_sleep():
    async def cal_sleep(name, date, delay, invoker_id, result=None, *, loop=None):
        coro = asyncio.sleep(delay, result=result, loop=loop)
        task = asyncio.create_task(coro)
        key = (name, date)
        try:
            cal_sleep.tasks[invoker_id][key] = task
        except KeyError:
            cal_sleep.tasks[invoker_id] = dict()
            cal_sleep.tasks[invoker_id][key] = task
        try:
            return await task
        except asyncio.CancelledError:
            raise
        finally:
            if len(cal_sleep.tasks[invoker_id]) == 0:
                del cal_sleep.tasks[invoker_id]
            else:
                del cal_sleep.tasks[invoker_id][key]

    cal_sleep.tasks = dict()
    cal_sleep.cancel = lambda key, inv_id: cal_sleep.tasks[inv_id][key].cancel()
    cal_sleep.display = lambda inv_id: ['    '.join(tup) for k, v in cal_sleep.tasks.items() if k == inv_id for tup in v.keys()]
    return cal_sleep

cal_sleep = cal_make_sleep()


class Calendar(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command()
    async def caladd(self, ctx, name: str, date_string: str):
        time_left = (datetime.fromisoformat(date_string) - datetime.today()).total_seconds()
        await ctx.send(f"'{name}' has been added to your calendar.")
        try:
            await cal_sleep(name, date_string, time_left, ctx.author.id)
        except asyncio.CancelledError:
            return None
        else:
            await ctx.send(name)

    @commands.command()
    async def calrm(self, ctx, name: str, date_string: str):
        key = (name, date_string)
        cal_sleep.cancel(key, ctx.author.id)
        await ctx.send(f"'{name}' has been removed from your calendar")

    @commands.command()
    async def cal(self, ctx):
        display = '\n'.join(cal_sleep.display(ctx.author.id))
        await ctx.send(display)

def setup(bot):
    bot.add_cog(Calendar(bot))
