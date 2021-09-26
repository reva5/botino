import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta

def make_sleep():
    async def sleep(delay, invoker_id, result=None, *, loop=None):
        coro = asyncio.sleep(delay, result=result, loop=loop)
        task = asyncio.create_task(coro)
        try:
            sleep.tasks[invoker_id].add(task)
        except KeyError:
            sleep.tasks[invoker_id] = set()
            sleep.tasks[invoker_id].add(task)
        try:
            return await task
        except asyncio.CancelledError:
            raise
        finally:
            sleep.tasks[invoker_id].remove(task)

    sleep.tasks = dict()
    sleep.cancel_all = lambda inv_id: sum(task.cancel() for k, v in sleep.tasks.items() if k == inv_id for task in v)
    return sleep

sleep = make_sleep()

class Timer(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
 
    @commands.command()
    async def timer(self, ctx, secs: int, msg: str = "Time's up!"):
        await ctx.send("Time's ticking...")
        try:
            await sleep(secs, ctx.author.id)
        except asyncio.CancelledError:
            return None
        else:
            await ctx.send(msg)

    @commands.command()
    async def canceltimers(self, ctx):
        sleep.cancel_all(ctx.author.id)
        await asyncio.wait(sleep.tasks[ctx.author.id])
        await ctx.send('Timers cancelled')

def setup(bot):
    bot.add_cog(Timer(bot))
