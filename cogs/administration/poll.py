import discord
from discord.ext import commands
import asyncio

class Poll(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def poll(self, ctx, *, qn: str):
        poll = discord.Embed(title='Poll:', type='rich', description=qn, colour=discord.Colour.random())
        poll.set_footer(text="React with \U0001F1FE for 'Yes'\nReact with \U0001F1F3 for 'No")
        message = await ctx.send(embed=poll)
        await message.add_reaction('\U0001F1FE')
        await message.add_reaction('\U0001F1F3')
        await asyncio.sleep(180)
        yes = (await message.channel.fetch_message(message.id)).reactions[0].count - 1
        no = (await message.channel.fetch_message(message.id)).reactions[1].count - 1
        replace_embed = discord.Embed(title=f"Poll results ('{qn}'):", type='rich', description=f"\U0001F1FE  'Yes': {yes}\n\U0001F1F3  'No': {no}", colour=discord.Colour.random())
        await message.edit(embed=replace_embed)
        await message.clear_reactions()

def setup(bot):
    bot.add_cog(Poll(bot))
