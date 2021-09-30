import discord
from discord.ext import commands
import aiohttp
import random
import asyncio
import html.parser

class Trivia(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def trivia(self, ctx):

        url = "https://opentdb.com/api.php"
        params = {"amount": 10, "type": "multiple"}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                if resp.status == 200:   
                    data = await resp.json(encoding='UTF-8')
                    correct_number = 0

                    for number in range(len(data["results"])):

                        category = data["results"][number]["category"]
                        type = data["results"][number]["type"]
                        difficulty = data["results"][number]["difficulty"]
                        question = html.parser.HTMLParser().unescape(data['results'][number]["question"])
                        correct_answer = data['results'][number]['correct_answer']
                        incorrect_answers = data['results'][number]['incorrect_answers']

                        answers = incorrect_answers.copy()
                        answers.append(correct_answer)
                        random.shuffle(answers)
                        ans_dict = {"\U0001F1E6": answers[0], "\U0001F1E7": answers[1], "\U0001F1E8": answers[2], "\U0001F1E9": answers[3]}
                        
                        for k, v in ans_dict.items():
                            if v == correct_answer:
                                correct_option = k
                                break
                        
                        embed = discord.Embed(
                                title=f'Question Nº{number+1}',
                                type='rich',
                                colour=discord.Colour.random(),
                                description=f'Category:`{category}`\nType:`{type}`\nDifficulty:`{difficulty}`'
                                )

                        embed.add_field(
                                name=question,
                                value=f'A. {answers[0]}\nB. {answers[1]}\nC. {answers[2]}\nD. {answers[3]}',
                                inline=False
                                )
                        
                        q = await ctx.send(embed=embed)
                        await q.add_reaction('\U0001F1E6')
                        await q.add_reaction('\U0001F1E7')
                        await q.add_reaction('\U0001F1E8')
                        await q.add_reaction('\U0001F1E9')

                        def check(reaction, user):
                            return user == ctx.author and reaction.message == q
                        

                        try:
                            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                        except asyncio.TimeoutError:
                            await ctx.send("Timeout reached. Trivia ended.")
                        else:
                            if str(reaction.emoji) == correct_option:
                                correct_number += 1
                                await ctx.send(f"Correct! {correct_number}/10")
                            else:
                                await ctx.send(f"Incorrect! {correct_number}/10")
                else:
                    await ctx.send("Couldn't connect to server. Sorry for the inconvenience!")

def setup(bot):
    bot.add_cog(Trivia(bot))
