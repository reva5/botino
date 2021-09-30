import discord
from discord.ext import commands
import aiohttp
import asyncio

class News(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def news(self, ctx, category: str, country: str, *, q: str):
        params = {"apiKey": '', "country": country, "category": category, "q": q}
        async with aiohttp.ClientSession() as session:
            async with session.get('https://newsapi.org/v2/top-headlines', params=params) as resp:
                data = await resp.json()
                
                await ctx.send(f"{len(data['articles'])} items found.")

                news = []

                for number in range(len(data['articles'])):
                    display = discord.Embed(
                            title=data['articles'][number]['title'],
                            type='rich',
                            url=data['articles'][number]['url'],
                            description=data['articles'][number]['description'],
                            colour=discord.Colour.random()
                            )

                    news.append(display)

                article = await ctx.send(embed=news[0])
                await article.add_reaction('➡️')

                def check(reaction, user):
                    return user == ctx.author and reaction.message == article

                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                except asyncio.TimeoutError:
                     await ctx.send("Timeout reached.")
                else:
                    try:
                        for number in range(1, len(data['articles'])):
                            await article.edit(embed=news[number])
                            try:
                                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                            except asyncio.TimeoutError:
                                 await ctx.send("Timeout reached.")
                            else:
                                pass
                    except IndexError:
                        pass


def setup(bot):
    bot.add_cog(News(bot))
