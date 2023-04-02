import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from scraper.menu import scrape_menus

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

@bot.command()
async def menu(ctx: commands.Context):
    embed = discord.Embed(
        title="Daegun Menu Scraper",
        description="It scrapes menus of DGHS",
        color=discord.Color.random()
    )
    menu_cards = scrape_menus()
    for menu_card in menu_cards:
        embed.add_field(
            name=menu_card.time,
            value=os.linesep.join(menu_card.menus),
            inline=True
        )
    await ctx.send(embed=embed)

bot.run(TOKEN)