import discord
from discord.ext import commands
import subprocess

class Calculator(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def calc(self, ctx, *, op: str):
        result = subprocess.check_output(f'python3 -c "print({op})"; exit 0',
                shell=True,
                encoding="UTF-8")
        try: await ctx.send(result)
        except discord.errors.HTTPException: await ctx.send("Please enter a valid operation.")

def setup(bot):
    bot.add_cog(Calculator(bot))

