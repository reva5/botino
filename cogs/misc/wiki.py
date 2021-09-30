import discord
from discord.ext import commands
import aiohttp
import asyncio

class Wikipedia(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def wiki(self, ctx, *, query: str):
        url = "https://en.wikipedia.org/w/api.php"
        params = {"action": "query", "list": "search", "srprop": "snippet", "format": "json", "origin": "*", "utf-8": "", "srsearch": query}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                data = await resp.json()
                print(data)

                await ctx.send(f"{len(data['query']['search'])} items found.")

                articles = []

                for number in range(len(data['query']['search'])):
                    display = discord.Embed(
                            title=data['query']['search'][number]['title'],
                            type='rich',
                            url=f"http://en.wikipedia.org/?curid={data['query']['search'][number]['pageid']}",
                            colour=discord.Colour.random()
                            )

                    articles.append(display)

                article = await ctx.send(embed=articles[0])
                await article.add_reaction('➡️')

                def check(reaction, user):
                    return user == ctx.author and reaction.message == article

                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                except asyncio.TimeoutError:
                     await ctx.send("Timeout reached.")
                else:
                    try:
                        for number in range(1, len(data['query']['search'])):
                            await article.edit(embed=articles[number])
                            try:
                                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                            except asyncio.TimeoutError:
                                 await ctx.send("Timeout reached.")
                            else:
                                pass
                    except IndexError:
                        pass
        
def setup(bot):
    bot.add_cog(Wikipedia(bot))
