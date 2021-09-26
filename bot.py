import discord
import os
from discord.ext import commands
import random

intents = discord.Intents.all()

bot = commands.Bot(command_prefix = '?', intents = intents, status = discord.Status.dnd, activity = discord.Game('touhou'))

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

for directory in os.listdir('./cogs'):
    for filename in os.listdir(f'./cogs/{directory}'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{directory}.{filename[:-3]}')

@bot.event
async def on_ready():
    print('Logged on as {0}!'.format(bot.user))
    print('Servers in which you are:')
    for guild in bot.guilds:
        print(guild.name)

@bot.event
async def on_message(message):
    print('Message from {0.author} ({0.guild}): {0.content}'.format(message))
    await bot.process_commands(message)

@bot.command()
async def stop(ctx):
    await bot.close()

@bot.command()
async def play(ctx):
    if ctx.author.voice.channel is not None:
        await ctx.author.voice.channel.connect()
    else:
        await ctx.send('Please connect to a voice channel.')

bot.run('ODkxNTcxMzQ4NzA5NzA3Nzg2.YVAShg.DCYANW8ObHZMX_jda_CesntMVUI')
