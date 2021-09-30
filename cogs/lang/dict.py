import discord
from discord.ext import commands
import aiohttp
import asyncio
import json

class Dictionary(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dict(self, ctx, word: str):
        low_word = word.lower()
        url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{low_word}'

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    data_json = await resp.json()

                    entry = discord.Embed(
                            title=data_json[0]['word'],
                            type='rich',
                            colour=discord.Colour.random(),
                            )

                    try:
                        entry.add_field(
                            name="Phonetics", 
                            value=data_json[0]['phonetics'][0]['text'],
                            inline=False
                            )
                    except:
                        pass

                    try:
                        entry.add_field(
                            name="Origin", 
                            value=data_json[0]['origin'],
                            inline=False
                            )
                    except:
                        pass

                    for num_mean in range(len(data_json[0]['meanings'])):
                        definitions = ''

                        for num_def in range(len(data_json[0]['meanings'][num_mean]['definitions'])):
                            definitions += f'\nDefinition {num_def+1}: {data_json[0]["meanings"][num_mean]["definitions"][num_def]["definition"]}'

                        entry.add_field(
                                name=f'Meaning {num_mean+1}',
                                value=f'__**Part of speech**__:\n{data_json[0]["meanings"][num_mean]["partOfSpeech"]}\n__**Definitions**__:{definitions}',
                                inline=False
                                )

                    await ctx.send(embed=entry)
        except KeyError:
            await ctx.send("Word not found!")

    @commands.command()
    async def dictesp(self, ctx, word: str):
        pass

def setup(bot):
    bot.add_cog(Dictionary(bot))

