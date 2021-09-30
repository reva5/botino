import discord
from discord.ext import commands
import googletrans

class Translator(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def translate(self, ctx, source: str, target: str, *, text: str):
        translator = googletrans.Translator()
        translated = translator.translate(text)
        embed = discord.Embed(
                title=f"{source} -> {target}",
                colour=discord.Colour.random(),
                description=f"```\n{translated.text}\n```"
                )
        await ctx.send(embed=embed)
    
    @commands.command()
    async def detect(self, ctx, *, text: str):
        translator = googletrans.Translator()
        detected = translator.detect(text)
        await ctx.send(f"Language: {detected.lang}\nConfidence level: {detected.confidence}")
        

def setup(bot):
    bot.add_cog(Translator(bot))
