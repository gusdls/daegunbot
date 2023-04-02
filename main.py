import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")

@bot.command()
async def ping(ctx: commands.Context):
    await ctx.send("pong!")

bot.run(TOKEN)