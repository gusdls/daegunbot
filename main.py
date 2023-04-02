import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from scraper.menu import scrape_menu
from scraper.news import scrape_news

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
        color=discord.Color.dark_magenta()
    )
    menu_cards = scrape_menu()
    for menu_card in menu_cards:
        embed.add_field(
            name=menu_card.time,
            value=os.linesep.join(menu_card.menu),
            inline=True
        )
    await ctx.send(embed=embed)

@bot.command()
async def news(ctx: commands.Context):
    news_list = scrape_news()
    for news in news_list:
        embed = discord.Embed(
            title=news.title,
            description=news.summary,
            url=news.url,
            color=discord.Color.greyple()
        )
        embed.set_thumbnail(url=news.thumbnail)
        embed.set_footer(text=news.press)
        await ctx.send(embed=embed)

bot.run(TOKEN)